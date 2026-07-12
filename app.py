import os
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from analyzer import analyze_contract, compare_contracts, parse_document, safe_filename, setup_qa_chain
from export_utils import (
    build_csv,
    build_docx_report,
    build_json_report,
    build_markdown_report,
    build_pdf_report,
)
import styles
import ui
import kyc_ui


APP_NAME = "ContractGuard"
MAX_FILE_BYTES = 25 * 1024 * 1024
SAMPLE_QUESTIONS = [
    "What should I negotiate before signing?",
    "Which termination terms deserve attention?",
    "What payment or renewal deadlines could I miss?",
]


class SampleFile:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.is_sample = True

    def read(self):
        return self.data


def configure_page():
    st.set_page_config(page_title=APP_NAME, page_icon="CG", layout="wide", initial_sidebar_state="expanded")
    st.markdown(styles.APP_CSS, unsafe_allow_html=True)


def initialize_state():
    defaults = {
        "analysis": None,
        "qa_chain": None,
        "chat_history": [],
        "messages": [],
        "file_processed": False,
        "source_name": None,
        "document_text": "",
        "document_quality": {},
        "review_history": [],
        "active_review_id": None,
        "review_context": {
            "party_role": "Not sure / general review",
            "jurisdiction": "",
            "goal": "Understand before signing",
            "risk_tolerance": "Balanced",
        },
        "comparison": None,
        "review_notes": "",
        "question_input": "",
        "workspace": "Contract review",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_workspace():
    for key, value in {
        "analysis": None,
        "qa_chain": None,
        "chat_history": [],
        "messages": [],
        "file_processed": False,
        "source_name": None,
        "document_text": "",
        "document_quality": {},
        "active_review_id": None,
        "comparison": None,
        "review_notes": "",
        "question_input": "",
    }.items():
        st.session_state[key] = value


def delete_current_review():
    review_id = st.session_state.active_review_id
    if review_id:
        st.session_state.review_history = [
            review for review in st.session_state.review_history if review.get("id") != review_id
        ]
    reset_workspace()


def summarize_report(report):
    counts = ui.risk_counts((report or {}).get("risk_assessment", []))
    return {
        "high": counts["high"],
        "medium": counts["medium"],
        "low": counts["low"],
        "missing": len((report or {}).get("missing_protections", [])),
    }


def save_current_review():
    report = st.session_state.analysis
    if not report:
        return
    review_id = st.session_state.active_review_id or str(uuid4())
    st.session_state.active_review_id = review_id
    existing = next(
        (review for review in st.session_state.review_history if review.get("id") == review_id),
        None,
    )
    review = {
        "id": review_id,
        "source_name": st.session_state.source_name or "Uploaded contract",
        "contract_type": report.get("contract_type") or "Unknown contract",
        "created_at": existing.get("created_at") if existing else datetime.now().strftime("%b %d, %Y %I:%M %p"),
        "analysis": report,
        "qa_chain": st.session_state.qa_chain,
        "chat_history": list(st.session_state.chat_history),
        "messages": list(st.session_state.messages),
        "summary": summarize_report(report),
        "document_text": st.session_state.document_text,
        "document_quality": dict(st.session_state.document_quality),
        "review_context": dict(st.session_state.review_context),
        "comparison": st.session_state.comparison,
        "review_notes": st.session_state.review_notes,
    }
    st.session_state.review_history = [
        review,
        *[item for item in st.session_state.review_history if item.get("id") != review_id],
    ]


def load_review(review_id):
    review = next(
        (item for item in st.session_state.review_history if item.get("id") == review_id),
        None,
    )
    if not review:
        return
    for key in (
        "analysis",
        "qa_chain",
        "document_text",
        "document_quality",
        "comparison",
        "review_notes",
    ):
        st.session_state[key] = review.get(key)
    st.session_state.chat_history = list(review.get("chat_history", []))
    st.session_state.messages = list(review.get("messages", []))
    st.session_state.review_context = dict(review.get("review_context", st.session_state.review_context))
    st.session_state.source_name = review.get("source_name")
    st.session_state.active_review_id = review_id
    st.session_state.file_processed = True


def friendly_error(exc):
    message = str(exc)
    lowered = message.lower()
    if "api" in lowered and ("key" in lowered or "401" in lowered):
        return "The analysis service is not configured correctly. Check the Groq API key."
    if "timeout" in lowered:
        return "The analysis service took too long to respond. Please retry in a moment."
    if "rate" in lowered or "429" in lowered:
        return "The analysis service is busy. Please wait briefly and retry."
    return f"ContractGuard could not complete this review: {message}"


def load_sample_contract():
    path = Path(__file__).with_name("sample_contracts") / "sample_lease.txt"
    if not path.exists():
        st.error("The sample lease is unavailable.")
        return None
    return SampleFile(path.read_bytes(), path.name)


def render_sidebar():
    uploaded_file = None
    consent = False
    with st.sidebar:
        ui.render_privacy_note()
        with st.expander("Review context", expanded=not st.session_state.file_processed):
            current = st.session_state.review_context
            party_options = [
                "Not sure / general review",
                "Tenant / buyer / customer",
                "Landlord / seller / provider",
                "Employee / contractor",
                "Employer / client",
                "Founder / company",
                "Other",
            ]
            party = st.selectbox(
                "Which side are you reviewing for?",
                party_options,
                index=party_options.index(current.get("party_role", party_options[0])) if current.get("party_role") in party_options else 0,
                disabled=st.session_state.file_processed,
            )
            jurisdiction = st.text_input(
                "Jurisdiction or governing law",
                value=current.get("jurisdiction", ""),
                placeholder="e.g. Lagos State, Nigeria",
                disabled=st.session_state.file_processed,
            )
            goal_options = ["Understand before signing", "Prepare to negotiate", "Prepare for counsel", "Check a revised version"]
            goal = st.selectbox(
                "Primary goal",
                goal_options,
                index=goal_options.index(current.get("goal", goal_options[0])) if current.get("goal") in goal_options else 0,
                disabled=st.session_state.file_processed,
            )
            tolerance_options = ["Conservative", "Balanced", "Commercially flexible"]
            tolerance = st.selectbox(
                "Risk posture",
                tolerance_options,
                index=tolerance_options.index(current.get("risk_tolerance", "Balanced")) if current.get("risk_tolerance") in tolerance_options else 1,
                disabled=st.session_state.file_processed,
            )
            if not st.session_state.file_processed:
                st.session_state.review_context = {
                    "party_role": party,
                    "jurisdiction": jurisdiction.strip(),
                    "goal": goal,
                    "risk_tolerance": tolerance,
                }

        st.markdown("#### Upload contract")
        uploaded_file = st.file_uploader(
            "PDF, DOCX, or TXT up to 25 MB",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            consent = st.checkbox(
                "I am authorised to process this document and understand that its text is sent to Groq.",
            )
        if st.button("Load sample lease", width="stretch"):
            uploaded_file = load_sample_contract()
            consent = True

        if st.session_state.file_processed:
            st.divider()
            st.caption(f"Current document: {st.session_state.source_name or 'Uploaded contract'}")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("New review", width="stretch"):
                    reset_workspace()
                    st.rerun()
            with col_b:
                if st.button("Delete", type="secondary", width="stretch"):
                    delete_current_review()
                    st.rerun()

        ui.render_review_history_intro(st.session_state.review_history)
        for review in st.session_state.review_history:
            ui.render_history_card(review, review.get("id") == st.session_state.active_review_id)
            if st.button("Open report", key=f"open-{review['id']}", width="stretch"):
                load_review(review["id"])
                st.rerun()
        if st.session_state.review_history:
            st.caption("History is stored only in this active app session.")
            if st.button("Clear session history", width="stretch"):
                st.session_state.review_history = []
                reset_workspace()
                st.rerun()
    return uploaded_file, consent


def process_upload(uploaded_file, consent):
    if not uploaded_file or st.session_state.file_processed:
        return
    if not consent:
        st.warning("Confirm the document-processing notice in the sidebar before analysis.")
        return
    data = uploaded_file.read()
    if len(data) > MAX_FILE_BYTES:
        st.error("This file is larger than 25 MB. Split or compress it before uploading.")
        return
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt"}:
        st.error("Supported file types are PDF, DOCX, and TXT.")
        return

    temp_path = None
    status = st.status("Preparing the contract review…", expanded=True)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name
        status.write("Extracting document text, running OCR when needed, and locating sources")
        full_text, chunks, quality = parse_document(temp_path)
        if not full_text.strip():
            status.update(label="No readable text found", state="error")
            st.error("No selectable text was found. Run OCR on scanned PDFs, then upload the searchable version.")
            return
        for warning in quality.get("warnings", []):
            st.warning(warning)
        if quality.get("ocr_used"):
            st.info("This PDF was image-based, so ContractGuard used OCR. Check names, dates, and amounts against the original scan.")
        status.write("Analysing clauses, obligations, payments, and negotiation priorities")
        report = analyze_contract(full_text, st.session_state.review_context)
        status.write("Building evidence retrieval for follow-up questions")
        qa_chain = setup_qa_chain(chunks, st.session_state.review_context)

        st.session_state.analysis = report
        st.session_state.qa_chain = qa_chain
        st.session_state.chat_history = []
        st.session_state.messages = []
        st.session_state.file_processed = True
        st.session_state.source_name = uploaded_file.name
        st.session_state.document_text = full_text
        st.session_state.document_quality = quality
        st.session_state.active_review_id = None
        st.session_state.comparison = None
        st.session_state.review_notes = ""
        save_current_review()
        status.update(label="Review ready", state="complete", expanded=False)
        st.rerun()
    except Exception as exc:
        status.update(label="Review could not be completed", state="error")
        st.error(friendly_error(exc))
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def render_chat():
    ui.render_chat_note()
    st.caption("Try one of these questions")
    columns = st.columns(3)
    for index, prompt in enumerate(SAMPLE_QUESTIONS):
        with columns[index]:
            if st.button(prompt, key=f"prompt-{index}", width="stretch"):
                st.session_state.question_input = prompt
                st.rerun()

    for message in st.session_state.messages:
        ui.render_chat_message(message["role"], message["content"], message.get("sources"))

    with st.form("contract-question", clear_on_submit=True):
        question = st.text_area(
            "Question",
            key="question_input",
            placeholder="Ask about termination, payment, repairs, renewal, notice, or any clause",
            height=100,
        )
        submitted = st.form_submit_button("Ask contract", width="stretch")
    if submitted:
        question = question.strip()
        if not question:
            st.warning("Enter a question first.")
            return
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Retrieving evidence and checking the contract…"):
            try:
                response = st.session_state.qa_chain.invoke(
                    {"input": question, "chat_history": st.session_state.chat_history}
                )
            except Exception as exc:
                st.error(friendly_error(exc))
                return
        answer = response["answer"]
        sources = response.get("sources", [])
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )
        st.session_state.chat_history.extend(
            [HumanMessage(content=question), AIMessage(content=answer)]
        )
        st.session_state.question_input = ""
        save_current_review()
        st.rerun()


def render_compare():
    st.markdown("### Compare a revised version")
    st.write("Upload a second version to identify substantive additions, removals, and risk changes. Formatting-only changes are ignored where possible.")
    revised = st.file_uploader("Revised PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], key="revised-file")
    if revised and st.button("Compare versions", width="stretch"):
        data = revised.read()
        if len(data) > MAX_FILE_BYTES:
            st.error("The revised file is larger than 25 MB.")
            return
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(revised.name).suffix.lower()) as temp_file:
                temp_file.write(data)
                temp_path = temp_file.name
            with st.spinner("Comparing substantive terms and risk…"):
                revised_text, _, quality = parse_document(temp_path)
                if not revised_text.strip():
                    st.error("No readable text was found in the revised version.")
                    return
                st.session_state.comparison = compare_contracts(
                    st.session_state.document_text,
                    revised_text,
                    st.session_state.review_context,
                )
                save_current_review()
        except Exception as exc:
            st.error(friendly_error(exc))
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    if st.session_state.comparison:
        ui.render_comparison(st.session_state.comparison)
        questions = st.session_state.comparison.get("questions_to_ask", [])
        if questions:
            st.markdown("#### Questions to ask about the revision")
            for item in questions:
                st.write(f"• {item}")


def render_exports(report):
    st.markdown("### Export and handoff")
    notes = st.text_area(
        "Private review notes",
        value=st.session_state.review_notes,
        placeholder="Add questions, decisions, or context for counsel. Notes stay in this app session and in exports you download.",
        height=140,
    )
    if notes != st.session_state.review_notes:
        st.session_state.review_notes = notes
        save_current_review()

    base = safe_filename(st.session_state.source_name.rsplit(".", 1)[0] if st.session_state.source_name else "contract-review")
    context = st.session_state.review_context
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "Download PDF",
            build_pdf_report(report, st.session_state.source_name, context, notes),
            file_name=f"{base}-contractguard-report.pdf",
            mime="application/pdf",
            width="stretch",
        )
    with col2:
        st.download_button(
            "Download DOCX",
            build_docx_report(report, st.session_state.source_name, context, notes),
            file_name=f"{base}-contractguard-report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width="stretch",
        )
    with col3:
        st.download_button(
            "Download Markdown",
            build_markdown_report(report, st.session_state.source_name, context, notes),
            file_name=f"{base}-contractguard-report.md",
            mime="text/markdown",
            width="stretch",
        )
    col4, col5, col6 = st.columns(3)
    with col4:
        st.download_button(
            "Obligations CSV",
            build_csv(report.get("obligations", [])),
            file_name=f"{base}-obligations.csv",
            mime="text/csv",
            disabled=not report.get("obligations"),
            width="stretch",
        )
    with col5:
        st.download_button(
            "Deadlines CSV",
            build_csv(report.get("deadlines", [])),
            file_name=f"{base}-deadlines.csv",
            mime="text/csv",
            disabled=not report.get("deadlines"),
            width="stretch",
        )
    with col6:
        st.download_button(
            "Raw JSON",
            build_json_report(report, context, st.session_state.document_quality),
            file_name=f"{base}-analysis.json",
            mime="application/json",
            width="stretch",
        )


def render_report(report):
    ui.render_report_header(
        report,
        st.session_state.source_name,
        st.session_state.document_quality,
    )
    warnings = st.session_state.document_quality.get("warnings", [])
    if warnings:
        st.warning("Extraction needs verification: " + " ".join(warnings))
    tabs = st.tabs(
        ["Overview", "Risks", "Negotiate", "Protections", "Obligations", "Ask", "Compare", "Export"]
    )
    with tabs[0]:
        ui.render_overview(report)
        with st.expander("Plain-English glossary"):
            ui.render_jargon(report)
    with tabs[1]:
        ui.render_risks(report)
    with tabs[2]:
        ui.render_negotiation(report)
    with tabs[3]:
        ui.render_missing_protections(report)
    with tabs[4]:
        ui.render_obligations(report)
    with tabs[5]:
        render_chat()
    with tabs[6]:
        render_compare()
    with tabs[7]:
        render_exports(report)


def main():
    configure_page()
    initialize_state()
    with st.sidebar:
        ui.render_sidebar_intro()
        workspace = st.radio(
            "Workspace",
            ["Contract review", "Verify onboarding"],
            key="workspace",
            horizontal=True,
        )
        if workspace == "Verify onboarding":
            kyc_ui.initialize_verify_state()
            kyc_ui.render_verify_sidebar()
    if workspace == "Verify onboarding":
        kyc_ui.render_verify_workspace()
        return
    uploaded_file, consent = render_sidebar()
    process_upload(uploaded_file, consent)
    if not st.session_state.file_processed:
        ui.render_empty_state()
        return
    report = st.session_state.analysis
    if not report:
        st.error("The report is unavailable. Start a new review and try again.")
        return
    render_report(report)


if __name__ == "__main__":
    main()
