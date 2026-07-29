from datetime import datetime

import streamlit as st

from kyc import evaluate_case, export_case, get_case, get_cases
from ui import safe_text


def _action_class(action):
    return {"Reject": "high", "Escalate": "medium", "Approve": "low"}.get(action, "medium")


def initialize_verify_state():
    defaults = {
        "kyc_case_id": get_cases()[0]["id"],
        "kyc_decisions": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_verify_sidebar():
    cases = get_cases()
    case_ids = [case["id"] for case in cases]
    current = st.session_state.kyc_case_id
    if current not in case_ids:
        current = case_ids[0]
    selected = st.selectbox(
        "Onboarding case",
        case_ids,
        index=case_ids.index(current),
        format_func=lambda case_id: f"{case_id} · {get_case(case_id)['applicant']}",
    )
    st.session_state.kyc_case_id = selected
    st.markdown(
        """
        <div class="ll-trust-note">
            <strong>Synthetic demonstration</strong>
            <p>Every identity and document in this workspace is fictional. Do not upload real identity documents in this milestone.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ll-history-title">Case queue</div>', unsafe_allow_html=True)
    for case in cases:
        evaluation = evaluate_case(case)
        active = " ll-history-card-active" if case["id"] == selected else ""
        action_class = _action_class(evaluation["suggested_action"])
        st.markdown(
            f"""
            <div class="ll-history-card{active}">
                <div class="ll-history-card-top">
                    <div><div class="ll-history-name">{safe_text(case['applicant'])}</div><div class="ll-history-source">{safe_text(case['id'])}</div></div>
                    <span class="{action_class}">{safe_text(evaluation['suggested_action'])}</span>
                </div>
                <div class="ll-history-metrics"><span>{evaluation['score']}/100 risk</span><span>{len(evaluation['findings'])} flags</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_verify_header(case, evaluation):
    action_class = _action_class(evaluation["suggested_action"])
    st.markdown(
        f"""
        <div class="ll-shell">
            <div class="ll-topbar">
                <div class="ll-nav-left"><div class="ll-dot"></div><div class="ll-top-label">Lenslayer Verify</div><div class="ll-chip">Synthetic case</div></div>
                <div class="ll-nav-right"><div class="ll-chip">Deterministic rules</div><div class="ll-chip">Evidence linked</div></div>
            </div>
            <header class="ll-report-header ll-verify-header">
                <div>
                    <div class="ll-kicker">Onboarding review</div>
                    <h1>{safe_text(case['applicant'])}</h1>
                    <div class="ll-meta">{safe_text(case['id'])} · Submitted {safe_text(case['submitted_at'].replace('T', ' '))}</div>
                    <div class="ll-meta">Synthetic identity reconciliation case</div>
                </div>
                <span class="ll-pill ll-pill-{action_class}">Suggested: {safe_text(evaluation['suggested_action'])}</span>
            </header>
            <div class="ll-summary-strip ll-verify-summary" aria-label="Case summary">
                <div><strong class="{action_class}">{evaluation['score']}</strong><span>Risk score</span></div>
                <div><strong>{len(evaluation['findings'])}</strong><span>Discrepancies</span></div>
                <div><strong>{evaluation['document_count']}/{evaluation['required_document_count']}</strong><span>Documents</span></div>
                <div><strong>{evaluation['average_confidence']:.0%}</strong><span>Extraction confidence</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(evaluation):
    action_class = _action_class(evaluation["suggested_action"])
    st.markdown(
        f"""
        <div class="ll-verify-brief">
            <div><div class="ll-kicker">Compliance summary</div><p>{safe_text(evaluation['summary'])}</p></div>
            <div class="ll-verify-recommendation"><span>Recommended action</span><strong class="{action_class}">{safe_text(evaluation['suggested_action'])}</strong><p>{safe_text(evaluation['reasoning'])}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h2 class='ll-section-title'>Flagged discrepancies</h2>", unsafe_allow_html=True)
    if not evaluation["findings"]:
        st.success("No discrepancies were detected by the configured rules.")
        return
    for index, finding in enumerate(evaluation["findings"], start=1):
        severity = finding["severity"].lower()
        st.markdown(
            f"""
            <article class="ll-risk-row ll-verify-finding">
                <div class="ll-risk-head">
                    <div><div class="ll-risk-index">{index:02d} · +{finding['points']} points</div><h2>{safe_text(finding['title'])}</h2></div>
                    <span class="ll-pill ll-pill-{severity}">{safe_text(finding['severity'])}</span>
                </div>
                <p>{safe_text(finding['explanation'])}</p>
                <div class="ll-label">Reviewer action</div><p>{safe_text(finding['action'])}</p>
            </article>
            """,
            unsafe_allow_html=True,
        )
        evidence = finding["evidence"]
        st.markdown(
            f"<div class='ll-evidence'><div class='ll-evidence-head'><span>Reconciliation evidence</span><span>{len(evidence)} source{'s' if len(evidence) != 1 else ''}</span></div></div>",
            unsafe_allow_html=True,
        )


def render_evidence(case, evaluation):
    st.markdown("<h2 class='ll-section-title'>Field reconciliation matrix</h2>", unsafe_allow_html=True)
    st.caption("Values are shown exactly as extracted from each synthetic source. Extraction confidence and risk are separate signals.")
    st.dataframe(evaluation["field_matrix"], width="stretch", hide_index=True)

    if evaluation["findings"]:
        st.markdown("<h2 class='ll-section-title'>Inspect a discrepancy</h2>", unsafe_allow_html=True)
        finding_index = st.selectbox(
            "Finding",
            range(len(evaluation["findings"])),
            format_func=lambda index: f"{evaluation['findings'][index]['severity']} · {evaluation['findings'][index]['title']}",
            label_visibility="collapsed",
        )
        finding = evaluation["findings"][finding_index]
        columns = st.columns(min(len(finding["evidence"]), 3))
        for index, item in enumerate(finding["evidence"]):
            with columns[index % len(columns)]:
                confidence = item["confidence"]
                st.markdown(
                    f"""
                    <div class="ll-evidence-panel">
                        <div class="ll-kicker">{safe_text(item['document'])}</div>
                        <h3>{safe_text(item['value'])}</h3>
                        <p>{safe_text(item['field'].replace('_', ' ').title())}</p>
                        <div class="ll-inline-meta">{safe_text(item['reference'])} · {confidence:.0%} confidence</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<h2 class='ll-section-title'>Document inventory</h2>", unsafe_allow_html=True)
    for document in case["documents"]:
        with st.expander(f"{document['label']} · {document['confidence']:.0%} extraction confidence"):
            st.caption(document["reference"])
            rows = [{"Field": key.replace("_", " ").title(), "Extracted value": value} for key, value in document["fields"].items()]
            st.dataframe(rows, width="stretch", hide_index=True)


def render_decision(case, evaluation):
    history = st.session_state.kyc_decisions.get(case["id"], [])
    st.markdown(
        f"""
        <div class="ll-ask-shell">
            <div class="ll-kicker">Human decision</div>
            <h2>Automation recommends. A reviewer decides.</h2>
            <p>The recommendation is explainable and reversible. Record the evidence considered and the reason for any override.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    options = ["Approve", "Escalate", "Reject"]
    with st.form(f"decision-{case['id']}"):
        decision = st.radio(
            "Decision",
            options,
            index=options.index(evaluation["suggested_action"]),
            horizontal=True,
        )
        rationale = st.text_area(
            "Reviewer rationale",
            placeholder="State which evidence supports the decision and what must happen next.",
            height=130,
        )
        submitted = st.form_submit_button("Record decision", width="stretch")
    if submitted:
        if not rationale.strip():
            st.warning("Add a reviewer rationale before recording the decision.")
        else:
            event = {
                "decision": decision,
                "rationale": rationale.strip(),
                "recommended_action": evaluation["suggested_action"],
                "recorded_at": datetime.now().isoformat(timespec="seconds"),
                "reviewer": "Session reviewer",
            }
            st.session_state.kyc_decisions.setdefault(case["id"], []).append(event)
            st.success("Decision recorded in this session's audit history.")
            st.rerun()

    st.markdown("<h2 class='ll-section-title'>Decision history</h2>", unsafe_allow_html=True)
    if not history:
        st.info("No reviewer decision has been recorded for this case.")
    for event in reversed(history):
        action_class = _action_class(event["decision"])
        st.markdown(
            f"""
            <div class="ll-audit-row">
                <div><span class="ll-pill ll-pill-{action_class}">{safe_text(event['decision'])}</span><strong>{safe_text(event['reviewer'])}</strong></div>
                <p>{safe_text(event['rationale'])}</p>
                <div class="ll-inline-meta">{safe_text(event['recorded_at'])} · System recommendation: {safe_text(event['recommended_action'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_queue(cases):
    rows = []
    for case in cases:
        evaluation = evaluate_case(case)
        rows.append(
            {
                "Case": case["id"],
                "Applicant": case["applicant"],
                "Risk score": evaluation["score"],
                "Flags": len(evaluation["findings"]),
                "Suggested action": evaluation["suggested_action"],
                "Average confidence": f"{evaluation['average_confidence']:.0%}",
            }
        )
    st.markdown("<h2 class='ll-section-title'>Synthetic onboarding queue</h2>", unsafe_allow_html=True)
    st.dataframe(rows, width="stretch", hide_index=True)
    st.caption("Queue ordering and service-level timers will be added with persistent case storage.")


def render_verify_workspace():
    initialize_verify_state()
    case = get_case(st.session_state.kyc_case_id)
    if not case:
        st.error("The selected synthetic case is unavailable.")
        return
    evaluation = evaluate_case(case)
    render_verify_header(case, evaluation)
    tabs = st.tabs(["Case review", "Evidence", "Decision", "Queue", "Export"])
    with tabs[0]:
        render_overview(evaluation)
    with tabs[1]:
        render_evidence(case, evaluation)
    with tabs[2]:
        render_decision(case, evaluation)
    with tabs[3]:
        render_queue(get_cases())
    with tabs[4]:
        st.markdown("### Export case package")
        st.write("Download the synthetic source data, reconciliation output, and session decision history as one audit-friendly JSON package.")
        payload = export_case(case, evaluation, st.session_state.kyc_decisions.get(case["id"], []))
        st.download_button(
            "Download case JSON",
            payload,
            file_name=f"{case['id'].lower()}-verify-case.json",
            mime="application/json",
            width="stretch",
        )
