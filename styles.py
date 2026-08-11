CONTRACTGUARD_MODULE_VERSION = 2


APP_CSS = """
<style>
:root {
    --cg-bg: #17191d;
    --cg-surface: #1e2126;
    --cg-surface-2: #252930;
    --cg-border: #343941;
    --cg-border-strong: #4a505a;
    --cg-text: #f1eee9;
    --cg-muted: #abaeb5;
    --cg-faint: #7f858e;
    --cg-accent: #d87967;
    --cg-accent-hover: #e58b79;
    --cg-red: #ef756e;
    --cg-amber: #d5a74d;
    --cg-green: #6db889;
    --cg-blue: #68a9d8;
}

html, body, [class*="css"], .stApp { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.stApp, [data-testid="stAppViewContainer"] { background: var(--cg-bg); color: var(--cg-text); }
[data-testid="stAppViewContainer"] main, [data-testid="stAppViewContainer"] main p,
[data-testid="stAppViewContainer"] main label, [data-testid="stAppViewContainer"] main li,
[data-testid="stAppViewContainer"] main h1, [data-testid="stAppViewContainer"] main h2,
[data-testid="stAppViewContainer"] main h3 { color: var(--cg-text); }
.block-container { max-width: 1160px; padding: 1.75rem 2rem 5rem; }

/* Preserve only the native sidebar controls. */
header[data-testid="stHeader"] { height: 3.5rem; min-height: 3.5rem; background: transparent; pointer-events: none; }
header[data-testid="stHeader"] [data-testid="stToolbar"] { background: transparent; pointer-events: none; }
header[data-testid="stHeader"] [data-testid="stToolbarActions"],
header[data-testid="stHeader"] [data-testid="stMainMenu"],
#MainMenu, footer, [data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"] { pointer-events: auto; z-index: 1001; }
[data-testid="stSidebarCollapsedControl"] button, [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"] button {
    min-width: 44px; min-height: 44px; color: var(--cg-text) !important; background: var(--cg-surface) !important;
    border: 1px solid var(--cg-border) !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] { background: #14161a; border-right: 1px solid var(--cg-border); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
[data-testid="stSidebar"] * { color: var(--cg-text); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] small { color: var(--cg-muted) !important; }

h1 a, h2 a, h3 a, [data-testid="stHeadingWithActionElements"] a { display: none !important; }

.cg-brand { display: flex; align-items: center; gap: .75rem; margin: .25rem 0 1.5rem; }
.cg-mark { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 8px; background: var(--cg-text); color: var(--cg-bg) !important; font-weight: 800; font-size: .82rem; }
.cg-brand-text { font-size: 1.05rem; font-weight: 700; }
.cg-brand-sub { margin-top: .1rem; color: var(--cg-muted) !important; font-size: .82rem; }
.cg-sidebar-heading { display: flex; justify-content: space-between; align-items: center; margin: 1.75rem 0 .75rem; color: var(--cg-muted); font-size: .84rem; font-weight: 650; }
.cg-sidebar-heading span { color: var(--cg-faint); }
.cg-history-row { padding: .8rem 0; border-top: 1px solid var(--cg-border); }
.cg-history-active { border-left: 1px solid var(--cg-accent); padding-left: .75rem; }
.cg-history-top { display: flex; gap: .5rem; align-items: center; justify-content: space-between; }
.cg-history-top strong { font-size: .9rem; font-weight: 650; }
.cg-current, .cg-status { display: inline-flex; align-items: center; min-height: 24px; padding: 2px 8px; border-radius: 999px; font-size: .76rem; font-weight: 700; white-space: nowrap; }
.cg-current { color: var(--cg-accent) !important; background: rgba(216,121,103,.11); }
.cg-history-source, .cg-history-summary { color: var(--cg-muted) !important; font-size: .8rem; line-height: 1.45; overflow-wrap: anywhere; }
.cg-history-source { margin-top: .25rem; }
.cg-history-summary { margin-top: .35rem; }

.cg-setup-header { max-width: 740px; margin: 1.5rem 0 2.5rem; }
.cg-product-row { display: flex; align-items: center; gap: .75rem; color: var(--cg-muted); font-size: .85rem; }
.cg-product-row strong { color: var(--cg-text); }
.cg-product-row span { padding-left: .75rem; border-left: 1px solid var(--cg-border); }
.cg-setup-header h1, .cg-report-header h1 { margin: 1.25rem 0 .65rem; font-size: clamp(2rem, 3vw, 2.65rem); line-height: 1.08; letter-spacing: -.03em; font-weight: 720; }
.cg-setup-header p { max-width: 650px; margin: 0; color: var(--cg-muted) !important; font-size: 1.08rem; line-height: 1.65; }
[data-testid="stVerticalBlockBorderWrapper"]:has([class*="st-key-review_setup"]) > div { border: 0 !important; background: transparent !important; padding: 0 !important; }
.st-key-review_setup { border: 0 !important; background: transparent !important; }
.cg-form-step { margin: 2.25rem 0 .85rem; padding-bottom: .65rem; border-bottom: 1px solid var(--cg-border); color: var(--cg-text); font-size: 1rem; font-weight: 700; }
.cg-field-note { margin: -.35rem 0 .75rem; color: var(--cg-muted) !important; font-size: .88rem; }
.cg-trust-note { margin: 1.2rem 0; padding: 1rem 0; border-top: 1px solid var(--cg-border); border-bottom: 1px solid var(--cg-border); }
.cg-trust-note strong { font-size: .9rem; }
.cg-trust-note p { margin: .35rem 0 0; color: var(--cg-muted) !important; font-size: .9rem; line-height: 1.55; }

/* Streamlit upload area styled as one drop zone. */
[data-testid="stFileUploaderDropzone"] { min-height: 150px; padding: 1.5rem !important; background: var(--cg-surface) !important; border: 1px dashed var(--cg-border-strong) !important; border-radius: 12px !important; }
[data-testid="stFileUploaderDropzone"] > div:first-child { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] > div:first-child { font-size: 0 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] > div:first-child:after { content: "Drop a contract here"; font-size: 1rem; font-weight: 700; color: var(--cg-text); }
[data-testid="stFileUploaderDropzoneInstructions"] small { font-size: 0 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small:after { content: "PDF, DOCX, or TXT · 25 MB maximum"; font-size: .88rem; color: var(--cg-muted); }
[data-testid="stFileUploaderDropzone"] button { min-width: 120px !important; height: 44px !important; min-height: 44px !important; }
[data-testid="stFileUploader"] [data-testid="stIconMaterial"] { display: none !important; }
[role="button"][aria-label^="Help for"], button[aria-label^="Help for"] { min-width: 44px !important; min-height: 44px !important; }

.cg-report-header { margin: 1.25rem 0 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--cg-border); }
.cg-report-title-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 1.5rem; }
.cg-report-header h1 { margin: .6rem 0 .45rem; }
.cg-report-header p { margin: 0; color: var(--cg-muted) !important; }
.cg-eyebrow { color: var(--cg-muted); font-size: .82rem; font-weight: 650; }
.cg-report-facts { display: flex; flex-wrap: wrap; gap: .55rem 1.25rem; margin-top: 1.35rem; color: var(--cg-muted); font-size: .86rem; }
.cg-synopsis { margin-top: 1.5rem !important; color: var(--cg-text) !important; font-size: 1.12rem; font-weight: 650; }
.cg-disclaimer { margin-top: .75rem; color: var(--cg-muted); font-size: .86rem; }
.cg-disclaimer strong { color: var(--cg-text); }
.cg-status-high { color: #ffd0cc; background: rgba(239,117,110,.15); }
.cg-status-medium { color: #f3d39a; background: rgba(213,167,77,.14); }
.cg-status-low { color: #a9dfbd; background: rgba(109,184,137,.13); }
.cg-status-needs-verification { color: #b9d9ef; background: rgba(104,169,216,.14); }

.cg-section-title { margin: 2rem 0 .75rem !important; font-size: 1.3rem !important; letter-spacing: -.01em !important; }
.cg-lead { max-width: 820px; color: var(--cg-text) !important; font-size: 1.05rem; line-height: 1.72; }
.cg-classification { display: grid; grid-template-columns: 1fr 1fr; margin: 1.5rem 0; border-top: 1px solid var(--cg-border); }
.cg-classification > div { display: flex; flex-direction: column; gap: .3rem; padding: .9rem 1rem .9rem 0; border-bottom: 1px solid var(--cg-border); }
.cg-classification > div:last-child { grid-column: 1 / -1; }
.cg-classification strong { font-size: .8rem; color: var(--cg-muted); }
.cg-classification span { line-height: 1.5; }
.cg-term-row, .cg-rule-row { display: grid; grid-template-columns: minmax(150px, .35fr) 1fr auto; gap: 1rem; padding: 1rem 0; border-top: 1px solid var(--cg-border); align-items: start; }
.cg-term-row p, .cg-term-row span { margin: 0; color: var(--cg-muted) !important; line-height: 1.55; }
.cg-term-row span { font-size: .82rem; }

.cg-finding { margin-top: 1.25rem; padding: 1.25rem; border: 1px solid var(--cg-border); border-radius: 12px; background: var(--cg-surface); }
.cg-finding-head { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }
.cg-finding-head span:first-child { color: var(--cg-muted); font-size: .78rem; }
.cg-finding h2, .cg-action-row h2, .cg-gap-row h2, .cg-change-row h2 { margin: .2rem 0 .5rem; font-size: 1.18rem; line-height: 1.3; }
.cg-finding h2 { font-size: 1.2rem !important; font-weight: 700 !important; }
.cg-finding-summary { margin: .25rem 0 1rem !important; color: var(--cg-muted) !important; line-height: 1.6; }
.cg-finding-body { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--cg-border); }
.cg-finding-body strong, .cg-gap-row strong { font-size: .82rem; color: var(--cg-muted); }
.cg-finding-body p { margin: .35rem 0 0; line-height: 1.58; }
.cg-finding-meta { display: flex; flex-wrap: wrap; gap: .55rem 1rem; margin-top: 1.1rem; padding-top: .85rem; border-top: 1px solid var(--cg-border); color: var(--cg-muted); font-size: .8rem; }
.cg-meta-item { color: var(--cg-muted); }
.cg-help { display: inline-grid; place-items: center; width: 18px; height: 18px; border: 1px solid var(--cg-border-strong); border-radius: 50%; cursor: help; }
.cg-evidence { margin: .6rem 0 1.35rem; padding: .95rem 1.1rem; border-left: 1px solid var(--cg-blue); background: rgba(104,169,216,.045); }
.cg-evidence-head { display: flex; justify-content: space-between; gap: 1rem; color: var(--cg-muted); font-size: .8rem; }
.cg-evidence-head strong { color: var(--cg-text); }
.cg-evidence blockquote { margin: .65rem 0 0; color: var(--cg-text); font-size: .95rem; line-height: 1.58; }

.cg-action-row { display: grid; grid-template-columns: 36px 1fr; gap: 1rem; padding: 1.25rem 0; border-top: 1px solid var(--cg-border); }
.cg-action-number { color: var(--cg-accent); font-weight: 750; }
.cg-action-row p { color: var(--cg-muted) !important; line-height: 1.55; }
.cg-action-row dl { display: grid; grid-template-columns: 80px 1fr; gap: .45rem 1rem; }
.cg-action-row dt { color: var(--cg-muted); font-size: .82rem; font-weight: 650; }
.cg-action-row dd { margin: 0; }
.cg-citation { color: var(--cg-muted); font-size: .8rem; }
.cg-gap-row, .cg-change-row { padding: 1.25rem 0; border-top: 1px solid var(--cg-border); }
.cg-gap-row > div { display: flex; align-items: center; gap: .75rem; }
.cg-gap-row p, .cg-change-row p { color: var(--cg-muted) !important; line-height: 1.55; }
.cg-playbook-head, .cg-tool-intro, .cg-comparison-head { margin-bottom: 1.25rem; }
.cg-playbook-head span { color: var(--cg-muted); font-size: .82rem; }
.cg-playbook-head h2, .cg-tool-intro h2 { margin: .2rem 0; font-size: 1.35rem; }
.cg-rule-row { grid-template-columns: minmax(180px, .38fr) 1fr; }
.cg-rule-row > div { display: flex; flex-direction: column; gap: .35rem; }
.cg-rule-row > div span, .cg-rule-row small { color: var(--cg-muted); }
.cg-rule-row p { margin: 0; }
.cg-rule-row small { grid-column: 2; }
.cg-locked { display: flex; gap: 1rem; padding: 1rem; border: 1px solid var(--cg-border); border-radius: 8px; background: var(--cg-surface); }
.cg-locked > span { font-size: 1.2rem; }
.cg-locked p { margin: .3rem 0 0; color: var(--cg-muted) !important; }
.cg-message { max-width: 820px; padding: 1rem 0; border-bottom: 1px solid var(--cg-border); }
.cg-message p { margin: .35rem 0 0; line-height: 1.6; }
.cg-message-user strong { color: var(--cg-accent); }

div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button, .stFormSubmitButton button {
    min-height: 44px; border-radius: 8px !important; border: 1px solid var(--cg-border-strong) !important;
    background: var(--cg-surface-2) !important; color: var(--cg-text) !important; font-weight: 650 !important;
}
div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { border-color: var(--cg-accent) !important; color: var(--cg-text) !important; }
button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background: var(--cg-accent) !important; border-color: var(--cg-accent) !important; color: #211715 !important; }
button[kind="primary"]:hover { background: var(--cg-accent-hover) !important; }
button:disabled { opacity: .42 !important; cursor: not-allowed !important; }
.st-key-delete_review_confirm button, .st-key-delete_all_confirm button { color: #ffd0cc !important; border-color: rgba(239,117,110,.65) !important; background: rgba(239,117,110,.10) !important; }

div[data-baseweb="select"] > div, input, textarea { min-height: 44px; border-radius: 8px !important; background: var(--cg-surface) !important; border-color: var(--cg-border) !important; color: var(--cg-text) !important; }
[data-baseweb="segmented-control"] { background: var(--cg-surface) !important; border-radius: 8px !important; padding: 3px; }
[data-baseweb="segmented-control"] button { min-height: 44px; border-radius: 6px !important; }
[data-testid="stExpander"] { border: 0 !important; border-top: 1px solid var(--cg-border) !important; border-radius: 0 !important; background: transparent !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--cg-border); border-radius: 8px; overflow: hidden; }
[data-testid="stDataFrame"] [data-testid="stElementToolbar"] { display: none !important; }

@media (max-width: 767px) {
    header[data-testid="stHeader"] { background: var(--cg-bg) !important; border-bottom: 1px solid var(--cg-border); }
    .block-container { padding: 1rem 1rem calc(5rem + env(safe-area-inset-bottom)); }
    body, p, label, li, input, textarea { font-size: 16px !important; }
    .cg-setup-header { margin-top: 2.5rem; }
    .cg-setup-header h1, .cg-report-header h1 { font-size: 2rem; }
    .cg-report-title-row { flex-direction: column; gap: .75rem; }
    .cg-report-facts { flex-direction: column; gap: .35rem; }
    .cg-synopsis { font-size: 1rem; line-height: 1.55; }
    .cg-classification, .cg-finding-body { grid-template-columns: 1fr; }
    .cg-classification > div:last-child { grid-column: auto; }
    .cg-finding { padding: 1rem; }
    .cg-finding-head { gap: .65rem; }
    .cg-finding-meta { flex-direction: column; }
    .cg-term-row, .cg-rule-row { grid-template-columns: 1fr; gap: .35rem; }
    .cg-rule-row small { grid-column: 1; }
    .cg-action-row dl { grid-template-columns: 1fr; }
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    [data-testid="column"] { min-width: 100% !important; width: 100% !important; flex: 1 1 100% !important; }
    [data-baseweb="segmented-control"] { width: 100%; overflow-x: auto; }
}
</style>
"""
