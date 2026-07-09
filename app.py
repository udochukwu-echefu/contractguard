import importlib
import os
import tempfile
from html import escape

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from analyzer import analyze_contract, parse_document, setup_qa_chain
import styles
import ui

styles = importlib.reload(styles)
ui = importlib.reload(ui)


APP_NAME = "ContractGuard"


class SampleFile:
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def read(self):
        return self.data


def configure_page():
    st.set_page_config(page_title=APP_NAME, layout="wide")
    st.markdown(styles.APP_CSS, unsafe_allow_html=True)


def initialize_state():
    defaults = {
        "analysis": None,
        "qa_chain": None,
        "chat_history": [],
        "messages": [],
        "file_processed": False,
        "source_name": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_workspace():
    st.session_state.analysis = None
    st.session_state.qa_chain = None
    st.session_state.chat_history = []
    st.session_state.messages = []
    st.session_state.file_processed = False
    st.session_state.source_name = None


def friendly_error(exc):
    message = str(exc)
    lowered = message.lower()
    if "connection error" in lowered or "connectionerror" in lowered:
        return (
            "Could not reach the model provider. Your API key is configured, so this is usually a temporary "
            "network or Groq API issue. Wait a moment, then try again."
        )
    if "401" in message or "unauthorized" in lowered or "invalid api key" in lowered:
        return "The Groq API key was rejected. Check GROQ_API_KEY in your .env file."
    if "rate limit" in lowered or "429" in message:
        return "Groq rate-limited this request. Wait a minute, then try again."
    if "model" in lowered and ("not found" in lowered or "does not exist" in lowered):
        return "The configured Groq model is unavailable. Update the model name in analyzer.py."
    return f"Unable to analyze this document: {message}"


def load_sample_contract():
    sample_path = os.path.join(os.path.dirname(__file__), "sample_contracts", "sample_lease.txt")
    if not os.path.exists(sample_path):
        st.error("Sample file not found.")
        return None

    with open(sample_path, "rb") as file:
        return SampleFile(file.read(), "sample_lease.txt")


def render_sidebar():
    uploaded_file = None

    with st.sidebar:
        ui.render_sidebar_intro()
        uploaded_file = st.file_uploader("Upload contract", type=["pdf", "txt"])

        if st.button("Load sample lease", use_container_width=True):
            uploaded_file = load_sample_contract()

        if st.session_state.file_processed:
            st.markdown('<div class="cg-sidebar-rule"></div>', unsafe_allow_html=True)
            st.caption(f"Current document: {st.session_state.source_name or 'Uploaded contract'}")
            if st.button("Start another review", use_container_width=True):
                reset_workspace()
                st.rerun()

    return uploaded_file


def process_upload(uploaded_file):
    if not uploaded_file or st.session_state.file_processed:
        return

    with st.spinner("Building the review report..."):
        suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        try:
            full_text, chunks = parse_document(temp_path)
            if not full_text.strip():
                st.error("No readable text was found in this document.")
                st.stop()

            st.session_state.analysis = analyze_contract(full_text)
            st.session_state.qa_chain = setup_qa_chain(chunks)
            st.session_state.chat_history = []
            st.session_state.messages = []
            st.session_state.file_processed = True
            st.session_state.source_name = uploaded_file.name
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(friendly_error(exc))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


def render_chat():
    ui.render_chat_note()

    for msg in st.session_state.messages:
        render_chat_message(msg["role"], msg["content"])

    with st.form("contract_question_form", clear_on_submit=True):
        user_q = st.text_area(
            "Question",
            placeholder="Ask about termination, rent, repairs, notice, or any clause",
            label_visibility="collapsed",
            height=120,
        )
        submitted = st.form_submit_button("Ask contract", use_container_width=True)

    if submitted and user_q.strip():
        question = user_q.strip()
        st.session_state.messages.append({"role": "user", "content": question})
        render_chat_message("user", question)

        with st.spinner("Searching the contract..."):
            response = st.session_state.qa_chain.invoke(
                {
                    "input": question,
                    "chat_history": st.session_state.chat_history,
                }
            )
            answer = response["answer"]

        render_chat_message("assistant", answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.chat_history.append(HumanMessage(content=question))
        st.session_state.chat_history.append(AIMessage(content=answer))


def render_chat_message(role, content):
    label = "You" if role == "user" else "ContractGuard"
    modifier = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="cg-message cg-message-{modifier}">
            <div class="cg-message-label">{label}</div>
            <p class="cg-message-copy">{escape(str(content))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report(report):
    ui.render_report_header(report, st.session_state.source_name)
    overview_tab, risks_tab, protections_tab, jargon_tab, chat_tab = st.tabs(
        ["Overview", "Risks", "Protections", "Plain English", "Ask"]
    )

    with overview_tab:
        ui.render_overview(report)

    with risks_tab:
        ui.render_risks(report)

    with protections_tab:
        ui.render_missing_protections(report)

    with jargon_tab:
        ui.render_jargon(report)

    with chat_tab:
        render_chat()


def main():
    configure_page()
    initialize_state()
    uploaded_file = render_sidebar()
    process_upload(uploaded_file)

    if not st.session_state.file_processed:
        ui.render_empty_state()
        return

    report = st.session_state.analysis
    if not report:
        st.error("Could not parse the contract analysis. Please try again.")
        return

    render_report(report)


if __name__ == "__main__":
    main()
