APP_CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap");

:root {
    --cg-bg: oklch(0.13 0.008 250);
    --cg-panel: oklch(0.17 0.01 250);
    --cg-panel-soft: oklch(0.20 0.012 250);
    --cg-border: oklch(0.29 0.012 250);
    --cg-border-strong: oklch(0.40 0.015 250);
    --cg-text: oklch(0.94 0.008 80);
    --cg-muted: oklch(0.70 0.012 250);
    --cg-faint: oklch(0.55 0.012 250);
    --cg-accent: oklch(0.68 0.17 25);
    --cg-accent-soft: oklch(0.23 0.045 25);
    --cg-high: oklch(0.67 0.20 25);
    --cg-medium: oklch(0.76 0.14 80);
    --cg-low: oklch(0.70 0.13 145);
    --cg-focus: oklch(0.78 0.13 25);
}

html, body, [class*="css"], .stApp { font-family: "Figtree", system-ui, sans-serif; }
.stApp { background: var(--cg-bg); color: var(--cg-text); }
[data-testid="stAppViewContainer"] { background: var(--cg-bg); }
[data-testid="stAppViewContainer"] main, [data-testid="stAppViewContainer"] main p,
[data-testid="stAppViewContainer"] main label, [data-testid="stAppViewContainer"] main li,
[data-testid="stAppViewContainer"] main h1, [data-testid="stAppViewContainer"] main h2,
[data-testid="stAppViewContainer"] main h3 { color: var(--cg-text); }
.block-container { max-width: 1180px; padding: 1.5rem 2rem 4rem; }

/* Keep Streamlit's header because its sidebar controls live inside it. Hide
   only the optional Cloud actions, never the toolbar container itself. */
header[data-testid="stHeader"] {
    height: 3.75rem;
    min-height: 3.75rem;
    background: transparent;
    border: 0;
    box-shadow: none;
    pointer-events: none;
}
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: transparent;
    pointer-events: none;
}
header[data-testid="stHeader"] [data-testid="stToolbarActions"],
header[data-testid="stHeader"] [data-testid="stMainMenu"] {
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] {
    top: .75rem;
    left: .75rem;
    z-index: 1001;
    pointer-events: auto;
}
[data-testid="stExpandSidebarButton"] {
    z-index: 1001;
    pointer-events: auto;
}
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    pointer-events: auto;
}
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
    min-width: 44px;
    min-height: 44px;
    color: var(--cg-text) !important;
    background: var(--cg-panel) !important;
    border: 1px solid var(--cg-border-strong) !important;
    border-radius: .65rem !important;
}

[data-testid="stSidebar"] { background: oklch(0.105 0.008 250); border-right: 1px solid var(--cg-border); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
[data-testid="stSidebar"] * { color: var(--cg-text); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] small { color: var(--cg-muted) !important; }

.cg-brand { display:flex; align-items:center; gap:.8rem; margin:.25rem 0 1.3rem; }
.cg-mark { width:2.75rem; height:2.75rem; display:grid; place-items:center; border:1px solid var(--cg-border-strong); border-radius:.8rem; background:var(--cg-panel); font-weight:800; }
.cg-brand-text { font-size:1.35rem; font-weight:800; line-height:1.05; }
.cg-top-label, .cg-kicker { color:var(--cg-muted); font-size:.72rem; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }
.cg-brand .cg-top-label { margin-top:.3rem; }
.cg-sidebar-copy { color:var(--cg-muted) !important; font-size:.96rem; line-height:1.55; }
.cg-trust-note { border:1px solid var(--cg-border); border-radius:.75rem; padding:.85rem; margin:.9rem 0 1.1rem; background:var(--cg-panel); }
.cg-trust-note strong { font-size:.82rem; }
.cg-trust-note p { color:var(--cg-muted) !important; font-size:.78rem; line-height:1.45; margin:.4rem 0 0; }
.cg-sidebar-rule { height:1px; background:var(--cg-border); margin:1.5rem 0 1.1rem; }
.cg-history-title { font-size:.75rem; text-transform:uppercase; letter-spacing:.09em; font-weight:800; }
.cg-history-count { color:var(--cg-muted); font-size:.78rem; margin:.25rem 0 .8rem; }
.cg-history-card { padding:.8rem; border:1px solid var(--cg-border); border-radius:.7rem; background:var(--cg-panel); margin:.45rem 0; }
.cg-history-card-active { border-color:oklch(0.62 0.08 80); }
.cg-history-card-top { display:flex; justify-content:space-between; gap:.7rem; }
.cg-history-name { font-size:.84rem; font-weight:750; }
.cg-history-source,.cg-history-date { color:var(--cg-muted); font-size:.69rem; }
.cg-history-date { text-align:right; max-width:6rem; }
.cg-history-metrics { display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.55rem; font-size:.68rem; }
.cg-history-metrics span { border:1px solid var(--cg-border); border-radius:999px; padding:.2rem .4rem; }
.cg-history-metrics .high,.high { color:var(--cg-high); }
.cg-history-metrics .medium,.medium { color:var(--cg-medium); }
.low { color:var(--cg-low); }

.cg-shell { width:100%; }
.cg-topbar { min-height:3.5rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; border-bottom:1px solid var(--cg-border); margin-bottom:2rem; }
.cg-nav-left,.cg-nav-right { display:flex; align-items:center; gap:.65rem; flex-wrap:wrap; }
.cg-dot { width:.65rem; height:.65rem; border-radius:50%; background:var(--cg-accent); }
.cg-chip,.cg-confidence { display:inline-flex; align-items:center; min-height:1.8rem; border:1px solid var(--cg-border); border-radius:999px; padding:.2rem .55rem; color:var(--cg-muted); font-size:.72rem; white-space:nowrap; }

.cg-setup-header { padding:2rem 0 1.5rem; }
.cg-setup-grid { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(18rem,.55fr); gap:3rem; align-items:end; }
.cg-setup-header h1 { margin:.65rem 0 .8rem; font-size:3.8rem; line-height:.94; letter-spacing:-.05em; font-weight:800; }
.cg-setup-header > .cg-setup-grid > div:first-child > p { max-width:62ch; margin:0; color:var(--cg-muted) !important; font-size:1.08rem; line-height:1.6; }
.cg-setup-outcome { padding-left:1.4rem; border-left:1px solid var(--cg-border); }
.cg-setup-outcome span { display:block; margin-bottom:.65rem; color:var(--cg-faint); font-size:.7rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
.cg-setup-outcome strong { display:block; font-size:1rem; line-height:1.4; }
.cg-setup-outcome p { margin:.55rem 0 0; color:var(--cg-muted) !important; font-size:.84rem; line-height:1.5; }

.st-key-review_setup { margin-top:1.25rem; }
.st-key-review_setup [data-testid="stForm"] { padding:1.35rem 1.4rem 1.45rem; border:1px solid var(--cg-border-strong); border-radius:1rem; background:var(--cg-panel); }
.st-key-review_setup [data-testid="stFileUploaderDropzone"] { min-height:8.5rem; display:flex; align-items:center; border-style:solid; background:oklch(0.145 0.012 250); }
.st-key-review_setup [data-testid="stFileUploader"] { margin-bottom:.4rem; }
.st-key-review_setup .cg-form-step { margin:2rem 0 .9rem; padding-top:1.1rem; border-top:1px solid var(--cg-border); color:var(--cg-accent); font-size:.72rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
.st-key-review_setup .cg-form-step:first-child { margin-top:0; padding-top:0; border-top:0; }
.st-key-review_setup .cg-trust-note { margin:1rem 0 .75rem; padding:.85rem 0; border:0; border-top:1px solid var(--cg-border); border-bottom:1px solid var(--cg-border); border-radius:0; background:transparent; }
.st-key-review_setup .cg-trust-note p { max-width:76ch; }
.st-key-review_setup [data-testid="stFormSubmitButton"] button { min-height:3.25rem; margin-top:.45rem; border-color:var(--cg-accent) !important; background:var(--cg-accent) !important; color:oklch(0.14 0.012 25) !important; font-size:1rem; }
.st-key-review_setup [data-testid="stFormSubmitButton"] button:hover { border-color:var(--cg-focus) !important; background:var(--cg-focus) !important; color:oklch(0.12 0.01 25) !important; }
.st-key-review_setup > div > div > .stButton button { background:transparent; }
.st-key-report_actions { margin:0 0 .6rem; }

.cg-hero { max-width:900px; padding:3rem 0 1.5rem; }
.cg-hero h1 { max-width:780px; margin:.8rem 0 1rem; font-size:clamp(3rem,7vw,6.2rem); line-height:.9; letter-spacing:-.055em; font-weight:800; }
.cg-hero-copy { max-width:68ch; color:var(--cg-muted) !important; font-size:1.15rem; line-height:1.6; }
.cg-signal-row { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); border-top:1px solid var(--cg-border); margin-top:2.5rem; }
.cg-signal { padding:1.1rem 1.25rem 1rem 0; }
.cg-signal + .cg-signal { border-left:1px solid var(--cg-border); padding-left:1.25rem; }
.cg-signal-code { color:var(--cg-accent); font-weight:800; font-size:.75rem; }
.cg-signal-title { margin:.55rem 0 .25rem; font-weight:750; }
.cg-signal p { color:var(--cg-muted) !important; font-size:.88rem; line-height:1.45; }
.cg-empty-note { max-width:70ch; border:1px solid var(--cg-border); border-radius:.75rem; padding:1rem 1.1rem; color:var(--cg-muted); background:var(--cg-panel); }

.cg-report-header { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; padding:1.2rem 0 1.4rem; }
.cg-report-header h1 { margin:.4rem 0 .55rem; max-width:760px; font-size:2.6rem; line-height:1.05; letter-spacing:-.035em; }
.cg-meta { color:var(--cg-muted); font-size:.88rem; line-height:1.55; }
.cg-pill { display:inline-flex; align-items:center; justify-content:center; min-height:2rem; padding:.25rem .65rem; border:1px solid currentColor; border-radius:999px; font-size:.72rem; font-weight:800; white-space:nowrap; }
.cg-pill-high { color:var(--cg-high); background:oklch(0.19 0.04 25); }
.cg-pill-medium { color:var(--cg-medium); background:oklch(0.19 0.035 80); }
.cg-pill-low { color:var(--cg-low); background:oklch(0.19 0.03 145); }
.cg-summary-strip { display:grid; grid-template-columns:repeat(5,1fr); border:1px solid var(--cg-border); border-radius:.9rem; background:var(--cg-panel); margin-bottom:1.2rem; }
.cg-summary-strip > div { display:flex; align-items:baseline; gap:.5rem; padding:.8rem 1rem; }
.cg-summary-strip > div + div { border-left:1px solid var(--cg-border); }
.cg-summary-strip strong { font-size:1.25rem; }
.cg-summary-strip span { color:var(--cg-muted); font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; }

div[data-testid="stTabs"] [data-baseweb="tab-list"] { position:sticky; top:0; z-index:5; background:var(--cg-bg); border-bottom:1px solid var(--cg-border); overflow-x:auto; scrollbar-width:thin; }
div[data-testid="stTabs"] button[role="tab"] { min-height:44px; padding:0 1rem; }
div[data-testid="stTabs"] button[role="tab"] p { color:var(--cg-muted); font-weight:700; white-space:nowrap; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color:var(--cg-text); }

.cg-section-title { margin:1.5rem 0 .7rem !important; font-size:1rem !important; letter-spacing:.01em !important; }
.cg-lead { max-width:70ch; font-size:1.08rem; line-height:1.65; color:var(--cg-muted) !important; }
.cg-panel,.cg-risk-row,.cg-priority,.cg-ask-shell,.cg-comparison-summary { border:1px solid var(--cg-border); border-radius:.85rem; background:var(--cg-panel); padding:1rem 1.1rem; margin:.75rem 0; }
.cg-panel-title { font-weight:750; margin-bottom:.3rem; }
.cg-panel p,.cg-risk-row p,.cg-priority p,.cg-ask-shell p { max-width:75ch; color:var(--cg-muted) !important; line-height:1.55; margin:.35rem 0; }
.cg-inline-meta { color:var(--cg-faint); font-size:.72rem; margin-top:.65rem; }
.cg-risk-row { padding:1.15rem; margin-top:1rem; border-bottom-left-radius:.25rem; border-bottom-right-radius:.25rem; }
.cg-risk-head { display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; }
.cg-risk-head h2 { margin:.2rem 0 .6rem; font-size:1.15rem; }
.cg-risk-index { color:var(--cg-accent); font-size:.72rem; font-weight:800; }
.cg-risk-clause { color:var(--cg-text) !important; font-weight:600; }
.cg-label { color:var(--cg-faint); font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; margin-top:.8rem; }
.cg-risk-meta { margin-top:.8rem; }
.cg-evidence { border:1px solid var(--cg-border); border-top:0; border-radius:.25rem .25rem .85rem .85rem; background:oklch(0.145 0.012 250); padding:.85rem 1rem; margin:0 0 1rem; }
.cg-evidence-head { display:flex; justify-content:space-between; gap:1rem; color:var(--cg-faint); font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
.cg-evidence blockquote { border:0; margin:.65rem 0 0; padding:0; color:var(--cg-muted); font-size:.9rem; line-height:1.5; }
.cg-priority { display:grid; grid-template-columns:2.2rem 1fr; gap:.8rem; }
.cg-priority-number { width:2rem; height:2rem; display:grid; place-items:center; border-radius:50%; background:var(--cg-accent-soft); color:var(--cg-accent); font-weight:800; }
.cg-priority h2,.cg-ask-shell h2,.cg-comparison-summary h2 { margin:0 0 .35rem; font-size:1.1rem; }
.cg-message { border:1px solid var(--cg-border); border-radius:.85rem; padding:.85rem 1rem; margin:.7rem 0; }
.cg-message-user { background:var(--cg-panel-soft); }
.cg-message-assistant { background:var(--cg-panel); }
.cg-message-label { color:var(--cg-faint); font-size:.68rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
.cg-message p { white-space:pre-wrap; line-height:1.55; margin:.35rem 0 0; }

.stButton > button,.stDownloadButton > button,button[kind="secondary"],button[kind="primary"] { min-height:44px; border-radius:.65rem; border:1px solid var(--cg-border-strong); font-weight:700; transition:background-color 180ms cubic-bezier(.25,1,.5,1),border-color 180ms cubic-bezier(.25,1,.5,1),color 180ms cubic-bezier(.25,1,.5,1); }
.stButton > button:hover,.stDownloadButton > button:hover { border-color:var(--cg-accent); color:var(--cg-text); }
button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,[role="tab"]:focus-visible { outline:3px solid var(--cg-focus) !important; outline-offset:2px; }
[data-testid="stFileUploaderDropzone"] { border-color:var(--cg-border-strong); background:var(--cg-panel); border-radius:.75rem; }
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-baseweb="select"] > div { background:var(--cg-panel) !important; border-color:var(--cg-border) !important; color:var(--cg-text) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--cg-border); border-radius:.75rem; overflow:hidden; }

@media (max-width:900px) {
    .block-container { padding:1rem 1rem 3rem; }
    .cg-topbar { align-items:flex-start; padding:.5rem 0; }
    .cg-nav-right { display:none; }
    .cg-setup-header { padding:1.4rem 0 1rem; }
    .cg-setup-grid { grid-template-columns:1fr; gap:1.4rem; }
    .cg-setup-header h1 { font-size:3rem; }
    .cg-setup-outcome { padding:.95rem 0 0; border-left:0; border-top:1px solid var(--cg-border); }
    .st-key-review_setup [data-testid="stForm"] { padding:1.1rem; }
    .st-key-report_actions { margin:0 0 .6rem; }
    .cg-hero { padding:1.6rem 0 1rem; }
    .cg-hero h1 { font-size:3rem; }
    .cg-signal-row { grid-template-columns:1fr; }
    .cg-signal + .cg-signal { border-left:0; border-top:1px solid var(--cg-border); padding-left:0; }
    .cg-report-header { flex-direction:column; }
    .cg-report-header h1 { font-size:2rem; }
    .cg-summary-strip { grid-template-columns:repeat(2,1fr); }
    .cg-summary-strip > div + div { border-left:0; }
    .cg-summary-strip > div:nth-child(even) { border-left:1px solid var(--cg-border); }
    .cg-summary-strip > div:nth-child(n+3) { border-top:1px solid var(--cg-border); }
    .cg-risk-head { flex-direction:column; }
}

@media (max-width:640px) {
    .cg-setup-header h1 { font-size:2.45rem; }
    .st-key-review_setup { margin-top:.65rem; }
    .st-key-review_setup [data-testid="stForm"] { padding:.9rem; border-radius:.8rem; }
    .cg-hero h1 { font-size:2.45rem; }
    .cg-summary-strip { grid-template-columns:1fr; }
    .cg-summary-strip > div:nth-child(even) { border-left:0; }
    .cg-summary-strip > div:nth-child(n+2) { border-top:1px solid var(--cg-border); }
    .cg-evidence-head { flex-direction:column; gap:.2rem; }
    .cg-priority { grid-template-columns:1fr; }
}

@media (prefers-reduced-motion:reduce) {
    *,*::before,*::after { scroll-behavior:auto !important; transition-duration:.01ms !important; animation-duration:.01ms !important; }
}
</style>
"""
