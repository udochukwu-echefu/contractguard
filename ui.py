from html import escape

import streamlit as st


def safe_text(value, fallback=""):
    text = fallback if value in (None, "") else str(value)
    return escape(text)


def severity_class(level):
    normalized = str(level or "").lower()
    return normalized if normalized in {"high", "medium", "low"} else "low"


def severity_pill(level):
    severity = severity_class(level)
    return f'<span class="cg-pill cg-pill-{severity}">{severity.title()} attention</span>'


def confidence_pill(confidence):
    value = str(confidence or "Medium").title()
    return f'<span class="cg-confidence">{safe_text(value)} confidence</span>'


def risk_counts(risks):
    counts = {"high": 0, "medium": 0, "low": 0}
    for risk in risks or []:
        counts[severity_class(risk.get("risk_level"))] += 1
    return counts


def render_sidebar_intro():
    st.markdown(
        """
        <div class="cg-brand">
            <div class="cg-mark">CG</div>
            <div>
                <div class="cg-brand-text">ContractGuard</div>
                <div class="cg-top-label">Clause intelligence</div>
            </div>
        </div>
        <p class="cg-sidebar-copy">Evidence-linked first-pass contract review, negotiation preparation, and document Q&amp;A.</p>
        """,
        unsafe_allow_html=True,
    )


def render_privacy_note():
    st.markdown(
        """
        <div class="cg-trust-note">
            <strong>Before you upload</strong>
            <p>Text is sent to Groq to generate the review and Q&amp;A. Embeddings are created in the app session. Temporary upload files are deleted after parsing. Do not upload material you are not authorised to process.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_review_history_intro(history):
    count = len(history)
    label = "Session history is empty" if count == 0 else f"{count} review{'s' if count != 1 else ''} in this session"
    st.markdown(
        f"""
        <div class="cg-sidebar-rule"></div>
        <div class="cg-history-title">Review history</div>
        <div class="cg-history-count">{safe_text(label)}</div>
        """,
        unsafe_allow_html=True,
    )


def render_history_card(review, is_active=False):
    summary = review.get("summary", {})
    active_class = " cg-history-card-active" if is_active else ""
    st.markdown(
        f"""
        <div class="cg-history-card{active_class}">
            <div class="cg-history-card-top">
                <div>
                    <div class="cg-history-name">{safe_text(review.get('contract_type'), 'Unknown contract')}</div>
                    <div class="cg-history-source">{safe_text(review.get('source_name'), 'Uploaded contract')}</div>
                </div>
                <div class="cg-history-date">{safe_text(review.get('created_at'))}</div>
            </div>
            <div class="cg-history-metrics" aria-label="Review summary">
                <span class="high">{summary.get('high', 0)} high</span>
                <span class="medium">{summary.get('medium', 0)} medium</span>
                <span>{summary.get('missing', 0)} possible gaps</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="cg-shell">
            <div class="cg-topbar">
                <div class="cg-nav-left"><div class="cg-dot"></div><div class="cg-top-label">ContractGuard</div><div class="cg-chip">Ready</div></div>
                <div class="cg-nav-right"><div class="cg-chip">PDF / DOCX / TXT</div><div class="cg-chip">Evidence linked</div></div>
            </div>
            <section class="cg-hero">
                <div class="cg-kicker">Contract review workspace</div>
                <h1>Know what deserves a second look.</h1>
                <p class="cg-hero-copy">Turn an agreement into a traceable first-pass report: priority risks, supporting clauses, negotiation asks, obligations, deadlines, and grounded follow-up answers.</p>
                <div class="cg-signal-row">
                    <div class="cg-signal"><div class="cg-signal-code">01</div><div class="cg-signal-title">Set your context</div><p>Tell ContractGuard which party you are and where the agreement applies.</p></div>
                    <div class="cg-signal"><div class="cg-signal-code">02</div><div class="cg-signal-title">Follow the evidence</div><p>Inspect the clause, location, confidence, and uncertainty behind each finding.</p></div>
                    <div class="cg-signal"><div class="cg-signal-code">03</div><div class="cg-signal-title">Prepare your next move</div><p>Export negotiation priorities, suggested language, questions, and obligations.</p></div>
                </div>
            </section>
            <div class="cg-empty-note"><strong>Start in the sidebar.</strong> Load the sample lease or upload a document you are authorised to review.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_header(analysis, source_name, quality=None):
    risks = analysis.get("risk_assessment", [])
    counts = risk_counts(risks)
    parties = ", ".join(analysis.get("parties_involved", [])) or "Not identified"
    quality = quality or {}
    st.markdown(
        f"""
        <div class="cg-shell">
            <div class="cg-topbar">
                <div class="cg-nav-left"><div class="cg-dot"></div><div class="cg-top-label">ContractGuard</div><div class="cg-chip">Report ready</div></div>
                <div class="cg-nav-right"><div class="cg-chip">{safe_text(quality.get('quality'), 'Parsed')}</div><div class="cg-chip">{'OCR · ' if quality.get('ocr_used') else ''}{quality.get('pages', 1)} page{'s' if quality.get('pages', 1) != 1 else ''}</div></div>
            </div>
            <header class="cg-report-header">
                <div>
                    <div class="cg-kicker">Review report</div>
                    <h1>{safe_text(analysis.get('title') or analysis.get('contract_type'), 'Contract review')}</h1>
                    <div class="cg-meta">{safe_text(analysis.get('contract_type'), 'Unknown type')} · {safe_text(parties)}</div>
                    <div class="cg-meta">Source: {safe_text(source_name, 'Uploaded document')} · Governing law: {safe_text(analysis.get('governing_law'), 'Not identified')}</div>
                </div>
                {severity_pill(analysis.get('overall_attention'))}
            </header>
            <div class="cg-summary-strip" aria-label="Review summary">
                <div><strong class="high">{counts['high']}</strong><span>High</span></div>
                <div><strong class="medium">{counts['medium']}</strong><span>Medium</span></div>
                <div><strong class="low">{counts['low']}</strong><span>Low</span></div>
                <div><strong>{len(analysis.get('missing_protections', []))}</strong><span>Possible gaps</span></div>
                <div><strong>{len(analysis.get('obligations', []))}</strong><span>Obligations</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_evidence(item):
    citation = safe_text(item.get("citation"), "Location not identified")
    quote = safe_text(item.get("quote"), "No exact excerpt returned")
    st.markdown(
        f"""
        <div class="cg-evidence">
            <div class="cg-evidence-head"><span>Document evidence</span><span>{citation}</span></div>
            <blockquote>{quote}</blockquote>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(analysis):
    st.markdown("<h2 class='cg-section-title'>Executive summary</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='cg-lead'>{safe_text(analysis.get('executive_summary'), 'No summary returned.')}</p>", unsafe_allow_html=True)
    uncertainties = analysis.get("uncertainties", [])
    if uncertainties:
        with st.expander(f"What this review could not verify ({len(uncertainties)})"):
            for item in uncertainties:
                st.write(f"• {item}")

    st.markdown("<h2 class='cg-section-title'>Key terms</h2>", unsafe_allow_html=True)
    for term in analysis.get("key_terms", []):
        st.markdown(
            f"<div class='cg-panel'><div class='cg-panel-title'>{safe_text(term.get('term'), 'Term')}</div><p>{safe_text(term.get('description'))}</p><div class='cg-inline-meta'>{safe_text(term.get('citation'), 'Location not identified')} · {safe_text(term.get('confidence'), 'Medium')} confidence</div></div>",
            unsafe_allow_html=True,
        )

    payments = analysis.get("payments", [])
    if payments:
        st.markdown("<h2 class='cg-section-title'>Payments</h2>", unsafe_allow_html=True)
        st.dataframe(payments, width="stretch", hide_index=True)


def render_risks(analysis):
    risks = sorted(
        analysis.get("risk_assessment", []),
        key=lambda item: {"high": 0, "medium": 1, "low": 2}[severity_class(item.get("risk_level"))],
    )
    if not risks:
        st.info("No clause risks were returned. This does not mean the contract is risk-free.")
        return
    for index, risk in enumerate(risks, start=1):
        st.markdown(
            f"""
            <article class="cg-risk-row">
                <div class="cg-risk-head"><div><div class="cg-risk-index">{index:02d}</div><h2>{safe_text(risk.get('title'), 'Clause finding')}</h2></div>{severity_pill(risk.get('risk_level'))}</div>
                <p class="cg-risk-clause">{safe_text(risk.get('clause'))}</p>
                <div class="cg-label">Why it matters</div><p>{safe_text(risk.get('explanation'))}</p>
                <div class="cg-label">Next step</div><p>{safe_text(risk.get('recommendation'))}</p>
                <div class="cg-risk-meta">{confidence_pill(risk.get('confidence'))}</div>
            </article>
            """,
            unsafe_allow_html=True,
        )
        render_evidence(risk)
        if risk.get("suggested_language"):
            with st.expander("Example replacement language"):
                st.write(risk["suggested_language"])
                st.caption("Starting point only. Have qualified counsel adapt language to your facts and jurisdiction.")


def render_negotiation(analysis):
    priorities = analysis.get("negotiation_priorities", [])
    if not priorities:
        st.info("No negotiation priorities were returned.")
        return
    for item in sorted(priorities, key=lambda entry: entry.get("priority", 99)):
        st.markdown(
            f"""
            <div class="cg-priority">
                <div class="cg-priority-number">{safe_text(item.get('priority'), '•')}</div>
                <div><h2>{safe_text(item.get('title'), 'Negotiation priority')}</h2><p>{safe_text(item.get('reason'))}</p>
                <div class="cg-label">Ask for</div><p>{safe_text(item.get('ask'))}</p>
                <div class="cg-label">Fallback</div><p>{safe_text(item.get('fallback'))}</p>
                <div class="cg-inline-meta">{safe_text(item.get('citation'), 'Location not identified')}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_missing_protections(analysis):
    items = analysis.get("missing_protections", [])
    if not items:
        st.success("No common protection gaps were detected in this pass. Verify with qualified counsel.")
        return
    st.caption("These items were not clearly detected. They are not confirmed legal omissions.")
    for item in items:
        st.markdown(
            f"<div class='cg-panel'><div class='cg-panel-title'>{safe_text(item.get('issue'), 'Possible protection gap')}</div><p>{safe_text(item.get('explanation'))}</p><div class='cg-label'>Verify</div><p>{safe_text(item.get('verification_note'))}</p><div class='cg-inline-meta'>{safe_text(item.get('confidence'), 'Medium')} confidence</div></div>",
            unsafe_allow_html=True,
        )
        if item.get("suggested_language"):
            with st.expander("Example language to discuss"):
                st.write(item["suggested_language"])


def render_obligations(analysis):
    obligations = analysis.get("obligations", [])
    deadlines = analysis.get("deadlines", [])
    if obligations:
        st.markdown("<h2 class='cg-section-title'>Responsibility matrix</h2>", unsafe_allow_html=True)
        st.dataframe(obligations, width="stretch", hide_index=True)
    else:
        st.info("No obligations were extracted.")
    if deadlines:
        st.markdown("<h2 class='cg-section-title'>Dates and notice triggers</h2>", unsafe_allow_html=True)
        st.dataframe(deadlines, width="stretch", hide_index=True)


def render_jargon(analysis):
    items = analysis.get("jargon_decoder", [])
    if not items:
        st.info("No legal terms were returned.")
        return
    for item in items:
        st.markdown(
            f"<div class='cg-panel'><div class='cg-panel-title'>{safe_text(item.get('term'), 'Term')}</div><p>{safe_text(item.get('plain_english'))}</p><div class='cg-inline-meta'>{safe_text(item.get('citation'), 'Location not identified')}</div></div>",
            unsafe_allow_html=True,
        )


def render_chat_note():
    st.markdown(
        """
        <div class="cg-ask-shell">
            <div class="cg-kicker">Document Q&amp;A</div>
            <h2>Ask the contract directly.</h2>
            <p>Answers cite the retrieved excerpts below them. If the evidence is incomplete, verify the full clause before relying on the answer.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role, content, sources=None):
    label = "You" if role == "user" else "ContractGuard"
    modifier = "user" if role == "user" else "assistant"
    st.markdown(
        f"<div class='cg-message cg-message-{modifier}'><div class='cg-message-label'>{label}</div><p>{safe_text(content)}</p></div>",
        unsafe_allow_html=True,
    )
    if sources:
        with st.expander(f"Evidence used ({len(sources)})"):
            for source in sources:
                st.markdown(f"**{source.get('label')} · {source.get('location')}**")
                st.caption(source.get("excerpt", ""))


def render_comparison(comparison):
    direction = comparison.get("risk_direction", "Mixed")
    st.markdown(
        f"<div class='cg-comparison-summary'><div class='cg-kicker'>Version comparison</div><h2>{safe_text(direction)}</h2><p>{safe_text(comparison.get('summary'))}</p></div>",
        unsafe_allow_html=True,
    )
    for change in comparison.get("changes", []):
        st.markdown(
            f"<div class='cg-panel'><div class='cg-panel-title'>{safe_text(change.get('category'))}: {safe_text(change.get('title'))}</div><div class='cg-label'>Before</div><p>{safe_text(change.get('before'))}</p><div class='cg-label'>After</div><p>{safe_text(change.get('after'))}</p><div class='cg-label'>Impact</div><p>{safe_text(change.get('impact'))}</p></div>",
            unsafe_allow_html=True,
        )
