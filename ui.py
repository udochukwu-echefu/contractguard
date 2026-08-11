from html import escape

import streamlit as st


CONTRACTGUARD_MODULE_VERSION = 2


def safe_text(value, fallback=""):
    return escape(fallback if value in (None, "") else str(value))


def severity_class(level):
    normalized = str(level or "").strip().lower()
    return normalized.replace(" ", "-") if normalized in {"high", "medium", "low", "needs verification"} else "needs-verification"


def severity_label(level):
    value = severity_class(level)
    return {"high": "High", "medium": "Medium", "low": "Low", "needs-verification": "Needs verification"}[value]


def severity_pill(level):
    severity = severity_class(level)
    return f'<span class="cg-status cg-status-{severity}">{severity_label(level)}</span>'


def confidence_pill(confidence):
    value = str(confidence or "Low").title()
    return f'<span class="cg-meta-item">Confidence: {safe_text(value)} <span class="cg-help" title="Confidence describes evidence and model certainty, not legal correctness.">?</span></span>'


def risk_counts(risks):
    counts = {"high": 0, "medium": 0, "low": 0, "needs-verification": 0}
    for risk in risks or []:
        counts[severity_class(risk.get("risk_level"))] += 1
    return counts


def render_sidebar_intro():
    st.markdown(
        """
        <div class="cg-brand">
            <div class="cg-mark">CG</div>
            <div><div class="cg-brand-text">ContractGuard</div><div class="cg-brand-sub">Review workspace</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_privacy_note():
    st.markdown(
        """
        <div class="cg-trust-note">
            <strong>How processing works</strong>
            <p>Extracted text is sent to Groq for analysis. Temporary upload files are deleted after parsing. Source text is retained only when you opt in.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_review_history_intro(history):
    count = len(history)
    st.markdown(
        f'<div class="cg-sidebar-heading">Review history <span>{count}</span></div>',
        unsafe_allow_html=True,
    )


def render_history_card(review, is_active=False):
    summary = review.get("summary", {})
    active_class = " cg-history-active" if is_active else ""
    current = '<span class="cg-current">Open</span>' if is_active else ""
    st.markdown(
        f"""
        <div class="cg-history-row{active_class}">
            <div class="cg-history-top"><strong>{safe_text(review.get('contract_type'), 'Contract review')}</strong>{current}</div>
            <div class="cg-history-source">{safe_text(review.get('source_name'), 'Uploaded document')}</div>
            <div class="cg-history-summary">{summary.get('high', 0)} high · {summary.get('medium', 0)} medium · {summary.get('missing', 0)} possible gaps</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_review_setup_header():
    st.markdown(
        """
        <div class="cg-setup-header">
            <div class="cg-product-row"><strong>ContractGuard</strong><span>New review</span></div>
            <h1>Review a contract</h1>
            <p>Upload the agreement, add the context that changes how it should be read, then confirm privacy choices.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _synopsis(analysis):
    counts = risk_counts(analysis.get("risk_assessment", []))
    needs_review = counts["high"] + counts["medium"] + counts["needs-verification"]
    gap_count = len(analysis.get("missing_protections", []))
    first = f"{needs_review} finding{'s' if needs_review != 1 else ''} need review."
    second = f" {counts['high']} {'are' if counts['high'] != 1 else 'is'} high."
    third = f" {gap_count} protection{'s' if gap_count != 1 else ''} may be missing."
    return first + second + third


def render_report_header(analysis, source_name, quality=None):
    parties = ", ".join(analysis.get("parties_involved", [])) or "Parties not identified"
    classification = analysis.get("classification", {})
    jurisdiction = analysis.get("governing_law") or "Not identified"
    st.markdown(
        f"""
        <header class="cg-report-header">
            <div class="cg-report-title-row">
                <div>
                    <div class="cg-eyebrow">Review report</div>
                    <h1>{safe_text(analysis.get('title') or analysis.get('contract_type'), 'Contract review')}</h1>
                    <p>{safe_text(analysis.get('contract_category'), 'General contract review')} · {safe_text(parties)}</p>
                </div>
                {severity_pill(analysis.get('overall_attention'))}
            </div>
            <div class="cg-report-facts">
                <span>Source: {safe_text(source_name, 'Uploaded document')}</span>
                <span>Governing law: {safe_text(jurisdiction)}</span>
                <span>Classification confidence: {safe_text(classification.get('confidence'), 'Needs verification')}</span>
            </div>
            <p class="cg-synopsis">{safe_text(_synopsis(analysis))}</p>
            <div class="cg-disclaimer"><strong>Not legal advice.</strong> This report supports first-pass review and human decision-making. Confidence does not mean legal correctness.</div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_evidence(item):
    st.markdown(
        f"""
        <div class="cg-evidence">
            <div class="cg-evidence-head"><strong>Source clause</strong><span>{safe_text(item.get('citation'), 'Location not identified')}</span></div>
            <blockquote>{safe_text(item.get('quote'), 'No exact excerpt returned')}</blockquote>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(analysis):
    st.markdown("<h2 class='cg-section-title'>Summary</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='cg-lead'>{safe_text(analysis.get('executive_summary'), 'No summary returned.')}</p>", unsafe_allow_html=True)
    classification = analysis.get("classification", {})
    st.markdown(
        f"""
        <div class="cg-classification">
            <div><strong>Contract type</strong><span>{safe_text(analysis.get('contract_category'), 'General contract review')}</span></div>
            <div><strong>Playbook</strong><span>{safe_text(analysis.get('playbook_evaluation', {}).get('playbook_name'), 'Not attached')}</span></div>
            <div><strong>Classification basis</strong><span>{safe_text(classification.get('reason'), 'Not available')}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uncertainties = analysis.get("uncertainties", [])
    if uncertainties:
        with st.expander(f"Needs verification ({len(uncertainties)})"):
            for item in uncertainties:
                st.write(f"• {item}")
    terms = analysis.get("key_terms", [])
    if terms:
        st.markdown("<h2 class='cg-section-title'>Key terms</h2>", unsafe_allow_html=True)
        for term in terms:
            st.markdown(
                f"<div class='cg-term-row'><strong>{safe_text(term.get('term'), 'Term')}</strong><p>{safe_text(term.get('description'))}</p><span>{safe_text(term.get('citation'), 'Location not identified')}</span></div>",
                unsafe_allow_html=True,
            )
    if analysis.get("payments"):
        st.markdown("<h2 class='cg-section-title'>Payments</h2>", unsafe_allow_html=True)
        st.dataframe(analysis["payments"], width="stretch", hide_index=True)


def render_risks(analysis):
    risks = sorted(
        analysis.get("risk_assessment", []),
        key=lambda item: {"high": 0, "medium": 1, "needs-verification": 2, "low": 3}[severity_class(item.get("risk_level"))],
    )
    if not risks:
        st.info("No findings were returned. This does not mean the contract is risk-free.")
        return
    for index, risk in enumerate(risks, start=1):
        jurisdiction = "Supplied" if risk.get("jurisdiction_supplied") else "Not supplied"
        st.markdown(
            f"""
            <article class="cg-finding">
                <div class="cg-finding-head"><div><span>Finding {index}</span><h2>{safe_text(risk.get('title'), 'Clause finding')}</h2></div>{severity_pill(risk.get('risk_level'))}</div>
                <p class="cg-finding-summary">{safe_text(risk.get('clause') or risk.get('explanation'))}</p>
                <div class="cg-finding-body">
                    <div><strong>Why this matters</strong><p>{safe_text(risk.get('explanation'))}</p></div>
                    <div><strong>Consequence</strong><p>{safe_text(risk.get('consequence'))}</p></div>
                    <div><strong>Reviewer action</strong><p>{safe_text(risk.get('recommendation'))}</p></div>
                </div>
                <div class="cg-finding-meta">
                    <span>Category: {safe_text(risk.get('applicable_category'), 'other')}</span>
                    {confidence_pill(risk.get('confidence'))}
                    <span>Jurisdiction: {jurisdiction}</span>
                    <span>Recommendation: {safe_text(risk.get('recommendation_scope'), 'General')}</span>
                    <span>Human state: {safe_text(risk.get('human_review_state'), 'Open')}</span>
                </div>
            </article>
            """,
            unsafe_allow_html=True,
        )
        render_evidence(risk)
        if risk.get("suggested_language"):
            with st.expander("Replacement language to discuss"):
                st.write(risk["suggested_language"])
                st.caption("Starting point only. Ask qualified counsel to adapt it to the facts and jurisdiction.")


def render_negotiation(analysis):
    priorities = analysis.get("negotiation_priorities", [])
    if not priorities:
        st.info("No negotiation priorities were returned.")
        return
    st.caption("General negotiation support. Confirm legal effect with qualified counsel in the applicable jurisdiction.")
    for item in sorted(priorities, key=lambda entry: entry.get("priority", 99)):
        jurisdiction = "Supplied" if item.get("jurisdiction_supplied") else "Not supplied"
        st.markdown(
            f"""
            <div class="cg-action-row"><span class="cg-action-number">{safe_text(item.get('priority'), '•')}</span><div>
                <h2>{safe_text(item.get('title'), 'Negotiation priority')}</h2><p>{safe_text(item.get('reason'))}</p>
                <dl><dt>Ask</dt><dd>{safe_text(item.get('ask'))}</dd><dt>Fallback</dt><dd>{safe_text(item.get('fallback'))}</dd></dl>
                <div class="cg-finding-meta"><span>{safe_text(item.get('citation'), 'Location not identified')}</span><span>Category: {safe_text(item.get('applicable_category'), 'other')}</span><span>Confidence: {safe_text(item.get('confidence'), 'Low')}</span><span>Jurisdiction: {jurisdiction}</span><span>Recommendation: {safe_text(item.get('recommendation_scope'), 'General')}</span><span>Human state: {safe_text(item.get('human_review_state'), 'Open')}</span></div>
            </div></div>
            """,
            unsafe_allow_html=True,
        )
        if item.get("quote"):
            render_evidence(item)


def render_missing_protections(analysis):
    items = analysis.get("missing_protections", [])
    if not items:
        st.success("No common protection gaps were detected in this pass. Verify with qualified counsel.")
        return
    st.caption("Potential gaps only. Confirm against the complete document and applicable law.")
    for item in items:
        st.markdown(
            f"<div class='cg-gap-row'><div>{severity_pill('Needs verification')}<h2>{safe_text(item.get('issue'), 'Possible protection gap')}</h2></div><p>{safe_text(item.get('explanation'))}</p><strong>Verify</strong><p>{safe_text(item.get('verification_note'))}</p></div>",
            unsafe_allow_html=True,
        )
        if item.get("suggested_language"):
            with st.expander("Language to discuss"):
                st.write(item["suggested_language"])


def render_obligations(analysis):
    if analysis.get("obligations"):
        st.markdown("<h2 class='cg-section-title'>Obligations</h2>", unsafe_allow_html=True)
        st.dataframe(analysis["obligations"], width="stretch", hide_index=True)
    else:
        st.info("No obligations were extracted.")
    if analysis.get("deadlines"):
        st.markdown("<h2 class='cg-section-title'>Dates and notice triggers</h2>", unsafe_allow_html=True)
        st.dataframe(analysis["deadlines"], width="stretch", hide_index=True)


def render_jargon(analysis):
    for item in analysis.get("jargon_decoder", []):
        st.markdown(f"**{safe_text(item.get('term'), 'Term')}**  \n{safe_text(item.get('plain_english'))}  \n*{safe_text(item.get('citation'), 'Location not identified')}*", unsafe_allow_html=True)


def render_playbook_evaluation(evaluation):
    if evaluation.get("category_mismatch"):
        st.error("This playbook does not match the classified contract type. The evaluation has been blocked.")
        return
    deviations = evaluation.get("deviations", [])
    if not deviations:
        st.info("No playbook evaluation is available for this report.")
        return
    st.markdown(f"<div class='cg-playbook-head'><span>Applied playbook</span><h2>{safe_text(evaluation.get('playbook_name'))}</h2></div>", unsafe_allow_html=True)
    for item in deviations:
        st.markdown(
            f"<div class='cg-rule-row'><div><strong>{safe_text(item.get('title'))}</strong><span>{safe_text(item.get('status'))}</span></div><p>{safe_text(item.get('preferred_position'))}</p><small>Matched finding: {safe_text(item.get('matched_finding'), 'Nothing detected')} · Semantic category: {safe_text(item.get('semantic_category'), 'Not matched')}</small></div>",
            unsafe_allow_html=True,
        )


def render_chat_note():
    st.markdown("<div class='cg-tool-intro'><h2>Ask the document</h2><p>Answers use retained source excerpts and show the evidence used.</p></div>", unsafe_allow_html=True)


def render_unavailable(title, explanation):
    st.markdown(f"<div class='cg-locked' role='status'><span aria-hidden='true'>🔒</span><div><strong>{safe_text(title)}</strong><p>{safe_text(explanation)}</p></div></div>", unsafe_allow_html=True)


def render_chat_message(role, content, sources=None):
    label = "You" if role == "user" else "ContractGuard"
    modifier = "user" if role == "user" else "assistant"
    st.markdown(f"<div class='cg-message cg-message-{modifier}'><strong>{label}</strong><p>{safe_text(content)}</p></div>", unsafe_allow_html=True)
    if sources:
        with st.expander(f"Evidence used ({len(sources)})"):
            for source in sources:
                st.markdown(f"**{source.get('label')} · {source.get('location')}**")
                st.caption(source.get("excerpt", ""))


def render_comparison(comparison):
    st.markdown(f"<div class='cg-comparison-head'><strong>{safe_text(comparison.get('risk_direction'), 'Mixed')}</strong><p>{safe_text(comparison.get('summary'))}</p></div>", unsafe_allow_html=True)
    for change in comparison.get("changes", []):
        st.markdown(f"<div class='cg-change-row'><span>{safe_text(change.get('category'))}</span><h2>{safe_text(change.get('title'))}</h2><strong>Before</strong><p>{safe_text(change.get('before'))}</p><strong>After</strong><p>{safe_text(change.get('after'))}</p><strong>Impact</strong><p>{safe_text(change.get('impact'))}</p></div>", unsafe_allow_html=True)
