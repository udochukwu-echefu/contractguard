from html import escape

import streamlit as st


def safe_text(value, fallback=""):
    text = fallback if value in (None, "") else str(value)
    return escape(text)


def severity_class(level):
    normalized = (level or "").lower()
    if normalized == "high":
        return "high"
    if normalized == "medium":
        return "medium"
    return "low"


def severity_pill(level):
    severity = severity_class(level)
    label = severity.title()
    return f'<span class="cg-pill cg-pill-{severity}">{label}</span>'


def risk_counts(risks):
    counts = {"high": 0, "medium": 0, "low": 0}
    for risk in risks:
        counts[severity_class(risk.get("risk_level"))] += 1
    return counts


def render_sidebar_intro():
    st.markdown(
        """
        <div class="cg-brand">
            <div class="cg-mark">CG</div>
            <div>
                <div class="cg-brand-text">ContractGuard</div>
                <div class="cg-top-label" style="margin-top:.35rem;">Clause intelligence</div>
            </div>
        </div>
        <p class="cg-sidebar-copy">
            Drop in a contract. Get a readable risk report, missing protection scan, and document-grounded follow-up chat.
        </p>
        <div class="cg-sidebar-note">
            Built for first-pass review. Use it to prepare better questions before signing or speaking with counsel.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="cg-shell">
        <div class="cg-topbar">
            <div class="cg-nav-left">
                <div class="cg-dot"></div>
                <div class="cg-top-label">ContractGuard</div>
                <div class="cg-chip">Ready for review</div>
            </div>
            <div class="cg-nav-right">
                <div class="cg-chip">PDF/TXT</div>
                <div class="cg-chip">Risk triage</div>
                <div class="cg-chip">Grounded Q&A</div>
            </div>
        </div>
        <div class="cg-stage">
            <div class="cg-hero-grid">
                <section class="cg-hero">
                    <div class="cg-kicker">Contract review workspace</div>
                    <h1>Read the fine print at full signal.</h1>
                    <p class="cg-hero-copy">
                        ContractGuard turns dense agreements into a focused review surface:
                        risky clauses, missing protections, plain-English terms, and grounded follow-up answers.
                    </p>
                    <div class="cg-hero-actions">
                        <div class="cg-action-primary">Load the sample lease from the sidebar</div>
                        <div class="cg-action-secondary">Or upload a PDF/TXT contract</div>
                    </div>
                    <div class="cg-signal-row">
                        <div class="cg-signal">
                            <div class="cg-signal-code">01</div>
                            <div class="cg-signal-title">Extract the shape</div>
                            <p class="cg-signal-copy">Parties, type, terms, and the clauses that control the deal.</p>
                        </div>
                        <div class="cg-signal">
                            <div class="cg-signal-code">02</div>
                            <div class="cg-signal-title">Rank the risk</div>
                            <p class="cg-signal-copy">High, medium, and low signals are separated so the report is scannable.</p>
                        </div>
                        <div class="cg-signal">
                            <div class="cg-signal-code">03</div>
                            <div class="cg-signal-title">Question the document</div>
                            <p class="cg-signal-copy">Ask follow-ups against retrieved contract context, not a generic answer.</p>
                        </div>
                    </div>
                </section>
                <aside class="cg-document">
                    <div class="cg-document-top">
                        <span>sample_lease.txt</span>
                        <span>analysis preview</span>
                    </div>
                    <div class="cg-paper">
                        <div class="cg-paper-title">Residential lease agreement</div>
                        <div class="cg-paper-line medium"></div>
                        <div class="cg-paper-line"></div>
                        <div class="cg-paper-line short"></div>
                        <div class="cg-paper-line medium"></div>
                        <div class="cg-finding">
                            <div class="cg-finding-label">High risk clause</div>
                            <p class="cg-finding-copy">
                                Rent is marked non-refundable even if the premises become uninhabitable.
                            </p>
                        </div>
                        <div class="cg-paper-line" style="margin-top:1.4rem;"></div>
                        <div class="cg-paper-line medium"></div>
                        <div class="cg-paper-line short"></div>
                    </div>
                </aside>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_header(analysis, source_name):
    risks = analysis.get("risk_assessment", [])
    counts = risk_counts(risks)
    parties = analysis.get("parties_involved", [])
    parties_text = ", ".join(parties) if parties else "Not identified"
    contract_type = safe_text(analysis.get("contract_type"), "Unknown contract")
    safe_source = safe_text(source_name, "Uploaded document")

    st.markdown(
        f"""
        <div class="cg-shell">
        <div class="cg-topbar">
            <div class="cg-nav-left">
                <div class="cg-dot"></div>
                <div class="cg-top-label">ContractGuard</div>
                <div class="cg-chip">Report generated</div>
            </div>
            <div class="cg-nav-right">
                <div class="cg-chip">PDF/TXT</div>
                <div class="cg-chip">Risk triage</div>
                <div class="cg-chip">Grounded Q&A</div>
            </div>
        </div>
        <div class="cg-stage">
            <div class="cg-report-header">
                <div>
                    <div class="cg-kicker">Review report</div>
                    <h1>{contract_type}</h1>
                    <div class="cg-meta">Parties: {safe_text(parties_text)}</div>
                    <div class="cg-meta">Source: {safe_source}</div>
                </div>
                <div class="cg-report-status">First pass review</div>
            </div>
            <div class="cg-summary-grid">
                <div class="cg-stat cg-stat-high">
                    <div class="cg-stat-label">High risk</div>
                    <div class="cg-stat-value">{counts["high"]}</div>
                </div>
                <div class="cg-stat cg-stat-medium">
                    <div class="cg-stat-label">Medium risk</div>
                    <div class="cg-stat-value">{counts["medium"]}</div>
                </div>
                <div class="cg-stat cg-stat-low">
                    <div class="cg-stat-label">Low risk</div>
                    <div class="cg-stat-value">{counts["low"]}</div>
                </div>
                <div class="cg-stat">
                    <div class="cg-stat-label">Missing protections</div>
                    <div class="cg-stat-value">{len(analysis.get("missing_protections", []))}</div>
                </div>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(analysis):
    key_terms = analysis.get("key_terms", [])
    if not key_terms:
        st.info("No key terms were returned for this contract.")
        return

    for term in key_terms:
        st.markdown(
            f"""
            <div class="cg-panel">
                <div class="cg-panel-title">{safe_text(term.get("term"), "Term")}</div>
                <p class="cg-panel-copy">{safe_text(term.get("description"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_risks(analysis):
    risks = analysis.get("risk_assessment", [])
    if not risks:
        st.info("No clause risks were returned for this contract.")
        return

    severity_order = {"high": 0, "medium": 1, "low": 2}
    sorted_risks = sorted(risks, key=lambda item: severity_order[severity_class(item.get("risk_level"))])

    for index, risk in enumerate(sorted_risks, start=1):
        clause = safe_text(risk.get("clause"), "Clause not provided")
        st.markdown(
            f"""
            <div class="cg-risk-row">
                <div class="cg-risk-head">
                    <div class="cg-risk-index">{index:02d}</div>
                    <div class="cg-risk-clause">{clause}</div>
                    {severity_pill(risk.get("risk_level"))}
                </div>
                <div class="cg-label">Why it matters</div>
                <p class="cg-panel-copy">{safe_text(risk.get("explanation"))}</p>
                <div class="cg-label">Suggested next step</div>
                <p class="cg-panel-copy">{safe_text(risk.get("recommendation"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_missing_protections(analysis):
    missing_items = analysis.get("missing_protections", [])
    if not missing_items:
        st.success("No missing protections were flagged in this pass.")
        return

    for item in missing_items:
        st.markdown(
            f"""
            <div class="cg-panel">
                <div class="cg-panel-title">{safe_text(item.get("issue"), "Missing protection")}</div>
                <p class="cg-panel-copy">{safe_text(item.get("explanation"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_jargon(analysis):
    jargon_items = analysis.get("jargon_decoder", [])
    if not jargon_items:
        st.info("No legal terms were returned for this contract.")
        return

    for item in jargon_items:
        st.markdown(
            f"""
            <div class="cg-panel">
                <div class="cg-panel-title">{safe_text(item.get("term"), "Term")}</div>
                <p class="cg-panel-copy">{safe_text(item.get("plain_english"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_chat_note():
    st.markdown(
        """
        <div class="cg-ask-shell">
            <div class="cg-ask-header">
                <div>
                    <div class="cg-kicker">Document Q&A</div>
                    <div class="cg-ask-title">Ask the contract directly.</div>
                    <p class="cg-ask-copy">
                        Answers use retrieved clauses from this document. If the context is missing, ContractGuard should say so.
                    </p>
                </div>
                <div class="cg-report-status">Grounded answers</div>
            </div>
            <div class="cg-prompt-grid">
                <div class="cg-prompt">What makes the termination clause risky?</div>
                <div class="cg-prompt">Who pays for repairs?</div>
                <div class="cg-prompt">What should I negotiate before signing?</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
