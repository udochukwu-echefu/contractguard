import os
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from analyzer import analyze_contract, chunks_from_text, compare_contracts, harden_report, parse_document, safe_filename, setup_qa_chain
from auth import require_identity
from export_utils import (
    build_csv,
    build_docx_report,
    build_json_report,
    build_markdown_report,
    build_pdf_report,
)
import styles
import ui
from playbooks import (
    CONTRACT_CATEGORIES,
    classify_contract,
    ensure_builtin_playbooks,
    evaluate_report,
    finding_key,
    playbook_for_category,
)
from storage import ReviewStore


APP_NAME = "ContractGuard"
MAX_FILE_BYTES = 25 * 1024 * 1024
SAMPLE_QUESTIONS = [
    "What should I negotiate before signing?",
    "Which termination terms deserve attention?",
    "What payment or renewal deadlines could I miss?",
]


@st.cache_resource
def get_store():
    return ReviewStore()


class SampleFile:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.is_sample = True

    def read(self):
        return self.data


def configure_page():
    st.set_page_config(page_title=APP_NAME, page_icon="CG", layout="wide", initial_sidebar_state="auto")
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
        "retain_source_text": False,
        "retention_days": 30,
        "active_playbook_id": None,
        "playbooks": [],
        "pending_review": None,
        "report_area": "Review",
        "review_section": "Summary",
        "actions_section": "Reviewer decisions",
        "tools_section": "Export and handoff",
        "notes_saved_at": None,
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
        "pending_review": None,
        "report_area": "Review",
        "review_section": "Summary",
        "actions_section": "Reviewer decisions",
        "tools_section": "Export and handoff",
    }.items():
        st.session_state[key] = value


def sync_workspace(store, identity):
    default_playbook = ensure_builtin_playbooks(store, identity.owner_id)
    st.session_state.playbooks = store.list_playbooks(identity.owner_id)
    if not st.session_state.active_playbook_id:
        st.session_state.active_playbook_id = default_playbook["id"]
    st.session_state.review_history = store.list_reviews(identity.owner_id)


def delete_current_review(store, identity):
    review_id = st.session_state.active_review_id
    if review_id:
        store.delete_review(identity.owner_id, review_id)
    reset_workspace()
    st.session_state.review_history = store.list_reviews(identity.owner_id)


def summarize_report(report):
    counts = ui.risk_counts((report or {}).get("risk_assessment", []))
    return {
        "high": counts["high"],
        "medium": counts["medium"],
        "low": counts["low"],
        "missing": len((report or {}).get("missing_protections", [])),
    }


def save_current_review(store, identity):
    report = st.session_state.analysis
    if not report:
        return
    review_id = st.session_state.active_review_id or str(uuid4())
    st.session_state.active_review_id = review_id
    review = {
        "id": review_id,
        "source_name": st.session_state.source_name or "Uploaded contract",
        "contract_type": report.get("contract_type") or "Unknown contract",
        "analysis": report,
        "messages": list(st.session_state.messages),
        "summary": summarize_report(report),
        "document_text": st.session_state.document_text,
        "document_quality": dict(st.session_state.document_quality),
        "review_context": dict(st.session_state.review_context),
        "comparison": st.session_state.comparison,
        "review_notes": st.session_state.review_notes,
        "retain_source_text": st.session_state.retain_source_text,
        "retention_days": st.session_state.retention_days,
        "playbook_id": st.session_state.active_playbook_id,
    }
    store.upsert_review(identity.owner_id, review)
    st.session_state.review_history = store.list_reviews(identity.owner_id)


def load_review(store, identity, review_id):
    review = store.get_review(identity.owner_id, review_id)
    if not review:
        return
    for key in (
        "analysis",
        "document_text",
        "document_quality",
        "comparison",
        "review_notes",
    ):
        st.session_state[key] = review.get(key)
    st.session_state.qa_chain = None
    st.session_state.messages = list(review.get("messages", []))
    st.session_state.chat_history = []
    for message in st.session_state.messages:
        content = message.get("content", "")
        if message.get("role") == "user":
            st.session_state.chat_history.append(HumanMessage(content=content))
        elif message.get("role") == "assistant":
            st.session_state.chat_history.append(AIMessage(content=content))
    st.session_state.review_context = dict(review.get("review_context", st.session_state.review_context))
    st.session_state.source_name = review.get("source_name")
    st.session_state.active_review_id = review_id
    st.session_state.file_processed = True
    st.session_state.retain_source_text = bool(review.get("retain_source_text"))
    st.session_state.retention_days = review.get("retention_days") or 30
    if review.get("playbook_id"):
        st.session_state.active_playbook_id = review["playbook_id"]
    updated_at = review.get("updated_at")
    try:
        st.session_state.notes_saved_at = datetime.fromisoformat(updated_at).astimezone().strftime("%b %d, %Y %I:%M %p") if updated_at else None
    except ValueError:
        st.session_state.notes_saved_at = updated_at


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


def render_sidebar(store, identity):
    with st.sidebar:
        account_label = identity.email or identity.name
        st.caption(f"Workspace owner: {account_label}")
        if identity.authenticated:
            if st.button("Sign out", width="stretch"):
                st.logout()
        elif store.config.local_only:
            st.caption("Local development mode · not for shared production use")

        ui.render_review_history_intro(st.session_state.review_history)
        for review in st.session_state.review_history:
            is_active = review.get("id") == st.session_state.active_review_id
            ui.render_history_card(review, is_active)
            if not is_active and st.button("Open review", key=f"open-{review['id']}", width="stretch"):
                load_review(store, identity, review["id"])
                st.rerun()
        if st.session_state.review_history:
            st.caption("Saved reviews are private to this workspace owner and expire under the selected retention policy.")
        with st.expander("Workspace settings"):
            if st.session_state.file_processed and st.session_state.active_review_id:
                affected = st.session_state.source_name or "current review"
                st.error(f"Delete {affected}? The report, decisions, and audit history will be removed permanently and cannot be recovered.")
                confirmation = st.text_input("Type the document filename to confirm", key="delete-review-name")
                if st.button(
                    f"Delete {affected}",
                    key="delete_review_confirm",
                    disabled=confirmation != affected,
                    width="stretch",
                ):
                    delete_current_review(store, identity)
                    st.rerun()
            if st.session_state.review_history:
                st.error("Delete every saved review? Reports, decisions, and audit history will be removed permanently and cannot be recovered.")
                delete_all = st.text_input("Type DELETE ALL to confirm", key="delete-all-name")
                if st.button("Delete all reviews", key="delete_all_confirm", disabled=delete_all != "DELETE ALL", width="stretch"):
                    store.clear_reviews(identity.owner_id)
                    st.session_state.review_history = []
                    reset_workspace()
                    st.rerun()


def render_review_setup(store, identity):
    ui.render_review_setup_header()
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
    goal_options = [
        "Understand before signing",
        "Prepare to negotiate",
        "Prepare for counsel",
        "Check a revised version",
    ]
    tolerance_options = ["Conservative", "Balanced", "Commercially flexible"]
    retention_options = [7, 30, 90, 365]
    retention_index = (
        retention_options.index(st.session_state.retention_days)
        if st.session_state.retention_days in retention_options
        else 1
    )

    with st.container(key="review_setup"):
        st.markdown("<div class='cg-form-step'>1. Add document</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Contract document", type=["pdf", "docx", "txt"], help="PDF, DOCX, or TXT up to 25 MB")

        st.markdown("<div class='cg-form-step'>2. Set context</div>", unsafe_allow_html=True)
        context_left, context_right = st.columns(2, gap="large")
        with context_left:
            party = st.selectbox("Review perspective", party_options, index=party_options.index(current.get("party_role", party_options[0])) if current.get("party_role") in party_options else 0)
            st.markdown("<p class='cg-field-note'>Changes which party's exposure and leverage the review prioritises.</p>", unsafe_allow_html=True)
            goal = st.selectbox("Primary goal", goal_options, index=goal_options.index(current.get("goal", goal_options[0])) if current.get("goal") in goal_options else 0)
            st.markdown("<p class='cg-field-note'>Shapes whether findings emphasise understanding, negotiation, or counsel handoff.</p>", unsafe_allow_html=True)
        with context_right:
            jurisdiction = st.text_input("Jurisdiction or governing law", value=current.get("jurisdiction", ""), placeholder="e.g. Lagos State, Nigeria")
            st.markdown("<p class='cg-field-note'>When blank, recommendations stay general and avoid enforceability claims.</p>", unsafe_allow_html=True)
            tolerance = st.selectbox("Risk posture", tolerance_options, index=tolerance_options.index(current.get("risk_tolerance", "Balanced")) if current.get("risk_tolerance") in tolerance_options else 1)
            st.markdown("<p class='cg-field-note'>Changes attention thresholds, not the meaning or legality of a clause.</p>", unsafe_allow_html=True)

        st.markdown("<div class='cg-form-step'>3. Confirm privacy and review</div>", unsafe_allow_html=True)
        retention_days = st.selectbox("Delete saved review after", retention_options, index=retention_index, format_func=lambda days: f"{days} days")
        retain_source_text = st.checkbox("Retain source text for reopened Q&A and comparison", value=st.session_state.retain_source_text, help="Off by default. The report is saved, but extracted contract text is discarded after this session.")
        ui.render_privacy_note()
        consent = st.checkbox("I am authorised to process this document and understand that its text is sent to Groq.")
        submitted = st.button("Review contract", type="primary", width="stretch", disabled=not uploaded_file or not consent)

        sample_clicked = st.button("Review the sample lease", key="main-sample-review", width="stretch")

    if submitted:
        st.session_state.review_context = {
            "party_role": party,
            "jurisdiction": jurisdiction.strip(),
            "goal": goal,
            "risk_tolerance": tolerance,
        }
        st.session_state.retention_days = retention_days
        st.session_state.retain_source_text = retain_source_text

    if sample_clicked:
        return load_sample_contract(), True, True
    return uploaded_file, consent, submitted


def process_upload(uploaded_file, consent, submitted, store, identity):
    if not submitted or st.session_state.file_processed:
        return
    if not uploaded_file:
        st.warning("Add a PDF, DOCX, or TXT contract before starting the review.")
        return
    if not consent:
        st.warning("Confirm that you are authorised to process this document before starting the review.")
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
        status.write("Classifying the document before selecting a review playbook")
        classification = classify_contract(full_text)
        if classification["requires_confirmation"]:
            st.session_state.pending_review = {
                "full_text": full_text,
                "quality": quality,
                "source_name": uploaded_file.name,
                "classification": classification,
            }
            status.update(label="Contract type needs confirmation", state="complete", expanded=False)
            st.rerun()
        finish_review(full_text, chunks, quality, uploaded_file.name, classification, store, identity, status)
    except Exception as exc:
        status.update(label="Review could not be completed", state="error")
        st.error(friendly_error(exc))
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def finish_review(full_text, chunks, quality, source_name, classification, store, identity, status=None):
    if status:
        status.write(f"Applying the {classification['contract_category']} playbook and analysing evidence")
    playbook = playbook_for_category(st.session_state.playbooks, classification["contract_category"])
    if not playbook:
        raise ValueError("No matching review playbook is available.")
    report = analyze_contract(full_text, st.session_state.review_context, classification)
    st.session_state.active_playbook_id = playbook["id"]
    report["playbook_evaluation"] = evaluate_report(report, playbook)
    if report["playbook_evaluation"].get("category_mismatch"):
        raise ValueError("The classified contract type and selected playbook do not agree.")
    if status:
        status.write("Building evidence retrieval for document questions")
    qa_chain = setup_qa_chain(chunks, st.session_state.review_context)
    st.session_state.analysis = report
    st.session_state.qa_chain = qa_chain
    st.session_state.chat_history = []
    st.session_state.messages = []
    st.session_state.file_processed = True
    st.session_state.source_name = source_name
    st.session_state.document_text = full_text
    st.session_state.document_quality = quality
    st.session_state.active_review_id = None
    st.session_state.comparison = None
    st.session_state.review_notes = ""
    st.session_state.pending_review = None
    save_current_review(store, identity)
    if status:
        status.update(label="Review ready", state="complete", expanded=False)
    st.rerun()


def render_classification_confirmation(store, identity):
    pending = st.session_state.pending_review
    if not pending:
        return
    classification = pending["classification"]
    ui.render_review_setup_header()
    st.warning("ContractGuard could not identify the agreement type with enough confidence to choose a specialist playbook.")
    st.markdown(f"**Document:** {pending['source_name']}  \n**Classification basis:** {classification['reason']}")
    selected = st.selectbox("Confirm the contract type", CONTRACT_CATEGORIES, index=CONTRACT_CATEGORIES.index(classification["contract_category"]))
    st.caption("This selection determines which clauses and protections ContractGuard checks. You can still review and edit the resulting human decisions.")
    confirm_col, cancel_col = st.columns(2)
    with confirm_col:
        confirm = st.button("Confirm type and continue", type="primary", width="stretch")
    with cancel_col:
        cancel = st.button("Cancel review", width="stretch")
    if cancel:
        st.session_state.pending_review = None
        st.rerun()
    if confirm:
        classification.update({"contract_category": selected, "confirmed_by_user": True, "requires_confirmation": False})
        status = st.status("Preparing the confirmed review…", expanded=True)
        try:
            finish_review(
                pending["full_text"],
                chunks_from_text(pending["full_text"]),
                pending["quality"],
                pending["source_name"],
                classification,
                store,
                identity,
                status,
            )
        except Exception as exc:
            status.update(label="Review could not be completed", state="error")
            st.error(friendly_error(exc))


def render_chat(store, identity):
    ui.render_chat_note()
    if st.session_state.qa_chain is None and not st.session_state.document_text:
        ui.render_unavailable("Ask the document is unavailable", "Source text was not retained for this review, so evidence retrieval cannot be rebuilt.")
        if st.button("Run a new review with source retention enabled", key="new-retained-ask"):
            reset_workspace()
            st.session_state.retain_source_text = True
            st.rerun()
        return
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
                if st.session_state.qa_chain is None:
                    st.session_state.qa_chain = setup_qa_chain(
                        chunks_from_text(st.session_state.document_text),
                        st.session_state.review_context,
                    )
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
        save_current_review(store, identity)
        st.rerun()


def render_compare(store, identity):
    st.markdown("### Compare a revised version")
    st.write("Upload a second version to identify substantive additions, removals, and risk changes. Formatting-only changes are ignored where possible.")
    if not st.session_state.document_text:
        ui.render_unavailable("Version comparison is unavailable", "Source text was not retained for this review, so there is no evidence baseline to compare against.")
        if st.button("Run a new review with source retention enabled", key="new-retained-compare"):
            reset_workspace()
            st.session_state.retain_source_text = True
            st.rerun()
        return
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
                save_current_review(store, identity)
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


def render_exports(report, store, identity):
    st.markdown("### Export and handoff")
    st.caption("Prepare context for counsel or another reviewer. The legal-advice disclosure is included in every report export.")
    notes = st.text_area(
        "Private handoff notes",
        value=st.session_state.review_notes,
        placeholder="Add questions, decisions, or context for counsel. Notes are saved with this review and included in exports.",
        height=140,
    )
    saved_label = st.session_state.notes_saved_at or "Not saved yet"
    st.caption(f"Last saved: {saved_label}")
    if st.button("Save handoff notes", disabled=notes == st.session_state.review_notes):
        st.session_state.review_notes = notes
        save_current_review(store, identity)
        st.session_state.notes_saved_at = datetime.now().astimezone().strftime("%b %d, %Y %I:%M %p")
        st.rerun()

    base = safe_filename(st.session_state.source_name.rsplit(".", 1)[0] if st.session_state.source_name else "contract-review")
    context = st.session_state.review_context
    st.download_button(
        "Download PDF",
        build_pdf_report(report, st.session_state.source_name, context, notes),
        file_name=f"{base}-contractguard-report.pdf",
        mime="application/pdf",
        type="primary",
        width="stretch",
        help="Best for a stable report that can be read, shared, and archived.",
    )
    with st.expander("Export options"):
        st.caption("DOCX · editable counsel handoff")
        st.download_button(
            "Download DOCX",
            build_docx_report(report, st.session_state.source_name, context, notes),
            file_name=f"{base}-contractguard-report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width="stretch",
        )
        st.caption("Markdown · portable notes and knowledge systems")
        st.download_button(
            "Download Markdown",
            build_markdown_report(report, st.session_state.source_name, context, notes),
            file_name=f"{base}-contractguard-report.md",
            mime="text/markdown",
            width="stretch",
        )
        st.caption("Obligations CSV · task and owner tracking")
        st.download_button(
            "Obligations CSV",
            build_csv(report.get("obligations", [])),
            file_name=f"{base}-obligations.csv",
            mime="text/csv",
            disabled=not report.get("obligations"),
            width="stretch",
        )
        st.caption("Deadlines CSV · calendar and deadline tracking")
        st.download_button(
            "Deadlines CSV",
            build_csv(report.get("deadlines", [])),
            file_name=f"{base}-deadlines.csv",
            mime="text/csv",
            disabled=not report.get("deadlines"),
            width="stretch",
        )
        st.caption("Raw JSON · structured integration or audit data")
        st.download_button(
            "Raw JSON",
            build_json_report(report, context, st.session_state.document_quality),
            file_name=f"{base}-analysis.json",
            mime="application/json",
            width="stretch",
        )


def render_playbook(report, store, identity):
    playbook = store.get_playbook(identity.owner_id, st.session_state.active_playbook_id)
    ui.render_playbook_evaluation(report.get("playbook_evaluation", {}))
    if not playbook:
        st.info("No review playbook is attached to this report.")
        return
    with st.expander("Playbook rule details"):
        st.caption(playbook.get("description", ""))
        for rule in playbook.get("rules", []):
            st.markdown(f"**{rule.get('title', 'Rule')}**  \nPreferred: {rule.get('preferred_position', '')}  \nEscalate when: {rule.get('escalation_trigger', '')}")


def render_decisions(report, store, identity):
    review_id = st.session_state.active_review_id
    if not review_id:
        st.info("Save the review before recording decisions.")
        return
    decisions = store.list_decisions(identity.owner_id, review_id)
    latest = {}
    for item in decisions:
        latest.setdefault(item["finding_key"], item)

    st.markdown("### Human review decisions")
    st.caption("AI findings and human decisions are separate. Each decision is timestamped and preserved in the audit history.")
    for index, finding in enumerate(report.get("risk_assessment", [])):
        key = finding_key(finding, index)
        previous = latest.get(key, {})
        with st.expander(f"{finding.get('risk_level', 'Review')} · {finding.get('title', 'Finding')}"):
            st.write(finding.get("explanation", ""))
            if finding.get("quote"):
                st.caption(f"{finding.get('citation', 'Location not identified')} · “{finding.get('quote')}”")
            with st.form(f"decision-{key}"):
                options = ["No decision", "Accept", "Reject", "Needs counsel", "Resolved"]
                prior_status = previous.get("status", "No decision")
                status = st.selectbox("Decision", options, index=options.index(prior_status) if prior_status in options else 0)
                assigned_to = st.text_input("Owner", value=previous.get("assigned_to", ""), placeholder="Name, role, or team")
                rationale = st.text_area("Add note", value=previous.get("rationale", ""), placeholder="Record why this decision was made and what should happen next")
                submitted = st.form_submit_button("Record decision")
            if submitted:
                store.record_decision(
                    identity.owner_id,
                    review_id,
                    {
                        "finding_key": key,
                        "finding_type": "risk",
                        "finding_title": finding.get("title") or "Finding",
                        "status": status,
                        "rationale": rationale,
                        "assigned_to": assigned_to,
                    },
                )
                st.rerun()

    if decisions:
        with st.expander("Decision history"):
            st.dataframe(decisions, width="stretch", hide_index=True)
    with st.expander("Review audit trail"):
        events = store.list_audit_events(identity.owner_id, review_id)
        if events:
            st.dataframe(events, width="stretch", hide_index=True)
        else:
            st.caption("No audit events yet.")


def navigate_report(area, section_key=None, section=None):
    st.session_state.report_area = area
    if section_key and section:
        st.session_state[section_key] = section


def canonical_contract_category(report):
    existing = report.get("contract_category") or report.get("classification", {}).get("contract_category")
    if existing in CONTRACT_CATEGORIES:
        return existing
    value = str(report.get("contract_type") or "").lower()
    if "commercial" in value and "lease" in value:
        return "Commercial lease"
    if "lease" in value or "tenancy" in value:
        return "Residential lease"
    if "employment" in value or "employee" in value:
        return "Employment agreement"
    if "non-disclosure" in value or "nda" in value or "confidentiality" in value:
        return "NDA"
    if "vendor" in value or "supplier" in value:
        return "Vendor agreement"
    if "service" in value or "consult" in value or "saas" in value:
        return "Service agreement"
    return "General contract review"


def reconcile_report_trust(report, store, identity):
    category = canonical_contract_category(report)
    playbook = playbook_for_category(st.session_state.playbooks, category)
    current_evaluation = report.get("playbook_evaluation", {})
    needs_update = (
        report.get("contract_category") != category
        or not report.get("classification")
        or not report.get("legal_disclaimer")
        or not playbook
        or current_evaluation.get("playbook_id") != (playbook or {}).get("id")
    )
    if not needs_update:
        return report
    classification = report.get("classification") or {
        "contract_category": category,
        "confidence": "Low",
        "reason": "Migrated from an earlier report. Confirm the type before relying on specialist playbook coverage.",
        "confirmed_by_user": False,
    }
    classification["contract_category"] = category
    report = harden_report(report, classification, st.session_state.review_context)
    if playbook:
        st.session_state.active_playbook_id = playbook["id"]
        report["playbook_evaluation"] = evaluate_report(report, playbook)
    st.session_state.analysis = report
    save_current_review(store, identity)
    return report


def render_report(report, store, identity):
    report = reconcile_report_trust(report, store, identity)
    with st.container(key="report_actions"):
        action_space, action_button = st.columns([3, 1])
        with action_button:
            if st.button("Review another contract", width="stretch"):
                reset_workspace()
                st.rerun()
    ui.render_report_header(
        report,
        st.session_state.source_name,
        st.session_state.document_quality,
    )
    warnings = st.session_state.document_quality.get("warnings", [])
    if warnings:
        st.warning("Extraction needs verification: " + " ".join(warnings))
    review_id = st.session_state.active_review_id
    if review_id:
        latest = {}
        for decision in store.list_decisions(identity.owner_id, review_id):
            latest.setdefault(decision["finding_key"], decision)
        for index, finding in enumerate(report.get("risk_assessment", [])):
            decision = latest.get(finding_key(finding, index))
            finding["human_review_state"] = decision.get("status") if decision else "No decision"

    st.caption("Guided sequence: Summary → Highest-risk findings → Decisions required → Negotiation plan → Handoff")
    area = st.segmented_control(
        "Report area",
        ["Review", "Actions", "Tools"],
        key="report_area",
        label_visibility="collapsed",
    ) or "Review"
    source_available = bool(st.session_state.document_text)

    if area == "Review":
        options = ["Summary", "Findings", "Missing protections", "Obligations and dates"]
        if st.session_state.review_section not in options:
            st.session_state.review_section = options[0]
        section = st.selectbox("Review section", options, key="review_section")
        if section == "Summary":
            ui.render_overview(report)
            render_playbook(report, store, identity)
            with st.expander("Plain-English glossary"):
                ui.render_jargon(report)
            st.button(
                "Continue to highest-risk findings",
                type="primary",
                on_click=navigate_report,
                args=("Review", "review_section", "Findings"),
            )
        elif section == "Findings":
            ui.render_risks(report)
            st.button(
                "Continue to decisions required",
                type="primary",
                on_click=navigate_report,
                args=("Actions", "actions_section", "Reviewer decisions"),
            )
        elif section == "Missing protections":
            ui.render_missing_protections(report)
        else:
            ui.render_obligations(report)
    elif area == "Actions":
        options = ["Reviewer decisions", "Negotiation plan"]
        if source_available:
            options.append("Ask the document")
        if st.session_state.actions_section not in options:
            st.session_state.actions_section = options[0]
        section = st.selectbox("Actions section", options, key="actions_section")
        if section == "Reviewer decisions":
            render_decisions(report, store, identity)
            st.button(
                "Continue to negotiation plan",
                type="primary",
                on_click=navigate_report,
                args=("Actions", "actions_section", "Negotiation plan"),
            )
        elif section == "Negotiation plan":
            ui.render_negotiation(report)
            st.button(
                "Continue to handoff",
                type="primary",
                on_click=navigate_report,
                args=("Tools", "tools_section", "Export and handoff"),
            )
        else:
            render_chat(store, identity)
        if not source_available:
            ui.render_unavailable("Ask the document unavailable", "This review was reopened without retained source text.")
            if st.button("Run a new review with source retention enabled", key="actions-new-retained"):
                reset_workspace()
                st.session_state.retain_source_text = True
                st.rerun()
    else:
        options = ["Export and handoff"]
        if source_available:
            options.insert(0, "Compare versions")
        if st.session_state.tools_section not in options:
            st.session_state.tools_section = options[-1]
        section = st.selectbox("Tools section", options, key="tools_section")
        if section == "Compare versions":
            render_compare(store, identity)
        else:
            render_exports(report, store, identity)
        if not source_available:
            ui.render_unavailable("Compare versions unavailable", "This review was reopened without retained source text.")
            if st.button("Run a new review with source retention enabled", key="tools-new-retained"):
                reset_workspace()
                st.session_state.retain_source_text = True
                st.rerun()


def main():
    configure_page()
    initialize_state()
    identity = require_identity()
    store = get_store()
    if not identity.authenticated and not store.config.local_only:
        st.error("A remote review database is configured without authentication. Enable OIDC before using this deployment.")
        st.stop()
    sync_workspace(store, identity)
    with st.sidebar:
        ui.render_sidebar_intro()
    render_sidebar(store, identity)
    if not st.session_state.file_processed:
        if st.session_state.pending_review:
            render_classification_confirmation(store, identity)
            return
        uploaded_file, consent, submitted = render_review_setup(store, identity)
        process_upload(uploaded_file, consent, submitted, store, identity)
        return
    report = st.session_state.analysis
    if not report:
        st.error("The report is unavailable. Start a new review and try again.")
        return
    render_report(report, store, identity)


if __name__ == "__main__":
    main()
