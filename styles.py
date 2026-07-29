APP_CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap");

:root {
    --ll-bg: oklch(0.13 0.008 250);
    --ll-panel: oklch(0.17 0.01 250);
    --ll-panel-soft: oklch(0.20 0.012 250);
    --ll-border: oklch(0.29 0.012 250);
    --ll-border-strong: oklch(0.40 0.015 250);
    --ll-text: oklch(0.94 0.008 80);
    --ll-muted: oklch(0.70 0.012 250);
    --ll-faint: oklch(0.55 0.012 250);
    --ll-accent: oklch(0.68 0.17 25);
    --ll-accent-soft: oklch(0.23 0.045 25);
    --ll-high: oklch(0.67 0.20 25);
    --ll-medium: oklch(0.76 0.14 80);
    --ll-low: oklch(0.70 0.13 145);
    --ll-focus: oklch(0.78 0.13 25);
}

html, body, [class*="css"], .stApp { font-family: "Figtree", system-ui, sans-serif; }
.stApp { background: var(--ll-bg); color: var(--ll-text); }
[data-testid="stAppViewContainer"] { background: var(--ll-bg); }
[data-testid="stAppViewContainer"] main, [data-testid="stAppViewContainer"] main p,
[data-testid="stAppViewContainer"] main label, [data-testid="stAppViewContainer"] main li,
[data-testid="stAppViewContainer"] main h1, [data-testid="stAppViewContainer"] main h2,
[data-testid="stAppViewContainer"] main h3 { color: var(--ll-text); }
.block-container { max-width: 1180px; padding: 1.5rem 2rem 4rem; }

/* Use Streamlit's minimal chrome mode and remove Community Cloud's remaining
   injected toolbar. Keep the sidebar reopen control available on small screens. */
header[data-testid="stHeader"] {
    height: 0;
    min-height: 0;
    background: transparent;
    border: 0;
    box-shadow: none;
}
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] {
    top: .75rem;
    left: .75rem;
    z-index: 1001;
}
[data-testid="stSidebarCollapsedControl"] button {
    min-width: 44px;
    min-height: 44px;
    color: var(--ll-text) !important;
    background: var(--ll-panel) !important;
    border: 1px solid var(--ll-border-strong) !important;
    border-radius: .65rem !important;
}

[data-testid="stSidebar"] { background: oklch(0.105 0.008 250); border-right: 1px solid var(--ll-border); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
[data-testid="stSidebar"] * { color: var(--ll-text); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] small { color: var(--ll-muted) !important; }

.ll-brand { display:flex; align-items:center; gap:.8rem; margin:.25rem 0 1.3rem; }
.ll-mark { width:2.75rem; height:2.75rem; display:grid; place-items:center; border:1px solid var(--ll-border-strong); border-radius:.8rem; background:var(--ll-panel); font-weight:800; }
.ll-brand-text { font-size:1.35rem; font-weight:800; line-height:1.05; }
.ll-top-label, .ll-kicker { color:var(--ll-muted); font-size:.72rem; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }
.ll-brand .ll-top-label { margin-top:.3rem; }
.ll-sidebar-copy { color:var(--ll-muted) !important; font-size:.96rem; line-height:1.55; }
.ll-trust-note { border:1px solid var(--ll-border); border-radius:.75rem; padding:.85rem; margin:.9rem 0 1.1rem; background:var(--ll-panel); }
.ll-trust-note strong { font-size:.82rem; }
.ll-trust-note p { color:var(--ll-muted) !important; font-size:.78rem; line-height:1.45; margin:.4rem 0 0; }
.ll-sidebar-rule { height:1px; background:var(--ll-border); margin:1.5rem 0 1.1rem; }
.ll-history-title { font-size:.75rem; text-transform:uppercase; letter-spacing:.09em; font-weight:800; }
.ll-history-count { color:var(--ll-muted); font-size:.78rem; margin:.25rem 0 .8rem; }
.ll-history-card { padding:.8rem; border:1px solid var(--ll-border); border-radius:.7rem; background:var(--ll-panel); margin:.45rem 0; }
.ll-history-card-active { border-color:oklch(0.62 0.08 80); }
.ll-history-card-top { display:flex; justify-content:space-between; gap:.7rem; }
.ll-history-name { font-size:.84rem; font-weight:750; }
.ll-history-source,.ll-history-date { color:var(--ll-muted); font-size:.69rem; }
.ll-history-date { text-align:right; max-width:6rem; }
.ll-history-metrics { display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.55rem; font-size:.68rem; }
.ll-history-metrics span { border:1px solid var(--ll-border); border-radius:999px; padding:.2rem .4rem; }
.ll-history-metrics .high,.high { color:var(--ll-high); }
.ll-history-metrics .medium,.medium { color:var(--ll-medium); }
.low { color:var(--ll-low); }

.ll-shell { width:100%; }
.ll-topbar { min-height:3.5rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; border-bottom:1px solid var(--ll-border); margin-bottom:2rem; }
.ll-nav-left,.ll-nav-right { display:flex; align-items:center; gap:.65rem; flex-wrap:wrap; }
.ll-dot { width:.65rem; height:.65rem; border-radius:50%; background:var(--ll-accent); }
.ll-chip,.ll-confidence { display:inline-flex; align-items:center; min-height:1.8rem; border:1px solid var(--ll-border); border-radius:999px; padding:.2rem .55rem; color:var(--ll-muted); font-size:.72rem; white-space:nowrap; }

.ll-setup-header { padding:2rem 0 1.5rem; }
.ll-setup-grid { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(18rem,.55fr); gap:3rem; align-items:end; }
.ll-setup-header h1 { margin:.65rem 0 .8rem; font-size:3.8rem; line-height:.94; letter-spacing:-.05em; font-weight:800; }
.ll-setup-header > .ll-setup-grid > div:first-child > p { max-width:62ch; margin:0; color:var(--ll-muted) !important; font-size:1.08rem; line-height:1.6; }
.ll-setup-outcome { padding-left:1.4rem; border-left:1px solid var(--ll-border); }
.ll-setup-outcome span { display:block; margin-bottom:.65rem; color:var(--ll-faint); font-size:.7rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
.ll-setup-outcome strong { display:block; font-size:1rem; line-height:1.4; }
.ll-setup-outcome p { margin:.55rem 0 0; color:var(--ll-muted) !important; font-size:.84rem; line-height:1.5; }

.st-key-review_setup { margin-top:1.25rem; }
.st-key-review_setup [data-testid="stForm"] { padding:1.35rem 1.4rem 1.45rem; border:1px solid var(--ll-border-strong); border-radius:1rem; background:var(--ll-panel); }
.st-key-review_setup [data-testid="stFileUploaderDropzone"] { min-height:8.5rem; display:flex; align-items:center; border-style:solid; background:oklch(0.145 0.012 250); }
.st-key-review_setup [data-testid="stFileUploader"] { margin-bottom:.4rem; }
.st-key-review_setup .ll-form-step { margin:2rem 0 .9rem; padding-top:1.1rem; border-top:1px solid var(--ll-border); color:var(--ll-accent); font-size:.72rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
.st-key-review_setup .ll-form-step:first-child { margin-top:0; padding-top:0; border-top:0; }
.st-key-review_setup .ll-trust-note { margin:1rem 0 .75rem; padding:.85rem 0; border:0; border-top:1px solid var(--ll-border); border-bottom:1px solid var(--ll-border); border-radius:0; background:transparent; }
.st-key-review_setup .ll-trust-note p { max-width:76ch; }
.st-key-review_setup [data-testid="stFormSubmitButton"] button { min-height:3.25rem; margin-top:.45rem; border-color:var(--ll-accent) !important; background:var(--ll-accent) !important; color:oklch(0.14 0.012 25) !important; font-size:1rem; }
.st-key-review_setup [data-testid="stFormSubmitButton"] button:hover { border-color:var(--ll-focus) !important; background:var(--ll-focus) !important; color:oklch(0.12 0.01 25) !important; }
.st-key-review_setup > div > div > .stButton button { background:transparent; }
.st-key-report_actions { margin:0 0 .6rem; }

.ll-hero { max-width:900px; padding:3rem 0 1.5rem; }
.ll-hero h1 { max-width:780px; margin:.8rem 0 1rem; font-size:clamp(3rem,7vw,6.2rem); line-height:.9; letter-spacing:-.055em; font-weight:800; }
.ll-hero-copy { max-width:68ch; color:var(--ll-muted) !important; font-size:1.15rem; line-height:1.6; }
.ll-signal-row { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); border-top:1px solid var(--ll-border); margin-top:2.5rem; }
.ll-signal { padding:1.1rem 1.25rem 1rem 0; }
.ll-signal + .ll-signal { border-left:1px solid var(--ll-border); padding-left:1.25rem; }
.ll-signal-code { color:var(--ll-accent); font-weight:800; font-size:.75rem; }
.ll-signal-title { margin:.55rem 0 .25rem; font-weight:750; }
.ll-signal p { color:var(--ll-muted) !important; font-size:.88rem; line-height:1.45; }
.ll-empty-note { max-width:70ch; border:1px solid var(--ll-border); border-radius:.75rem; padding:1rem 1.1rem; color:var(--ll-muted); background:var(--ll-panel); }

.ll-report-header { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; padding:1.2rem 0 1.4rem; }
.ll-report-header h1 { margin:.4rem 0 .55rem; max-width:760px; font-size:2.6rem; line-height:1.05; letter-spacing:-.035em; }
.ll-meta { color:var(--ll-muted); font-size:.88rem; line-height:1.55; }
.ll-pill { display:inline-flex; align-items:center; justify-content:center; min-height:2rem; padding:.25rem .65rem; border:1px solid currentColor; border-radius:999px; font-size:.72rem; font-weight:800; white-space:nowrap; }
.ll-pill-high { color:var(--ll-high); background:oklch(0.19 0.04 25); }
.ll-pill-medium { color:var(--ll-medium); background:oklch(0.19 0.035 80); }
.ll-pill-low { color:var(--ll-low); background:oklch(0.19 0.03 145); }
.ll-summary-strip { display:grid; grid-template-columns:repeat(5,1fr); border:1px solid var(--ll-border); border-radius:.9rem; background:var(--ll-panel); margin-bottom:1.2rem; }
.ll-summary-strip > div { display:flex; align-items:baseline; gap:.5rem; padding:.8rem 1rem; }
.ll-summary-strip > div + div { border-left:1px solid var(--ll-border); }
.ll-summary-strip strong { font-size:1.25rem; }
.ll-summary-strip span { color:var(--ll-muted); font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; }

div[data-testid="stTabs"] [data-baseweb="tab-list"] { position:sticky; top:0; z-index:5; background:var(--ll-bg); border-bottom:1px solid var(--ll-border); overflow-x:auto; scrollbar-width:thin; }
div[data-testid="stTabs"] button[role="tab"] { min-height:44px; padding:0 1rem; }
div[data-testid="stTabs"] button[role="tab"] p { color:var(--ll-muted); font-weight:700; white-space:nowrap; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color:var(--ll-text); }

.ll-section-title { margin:1.5rem 0 .7rem !important; font-size:1rem !important; letter-spacing:.01em !important; }
.ll-lead { max-width:70ch; font-size:1.08rem; line-height:1.65; color:var(--ll-muted) !important; }
.ll-panel,.ll-risk-row,.ll-priority,.ll-ask-shell,.ll-comparison-summary { border:1px solid var(--ll-border); border-radius:.85rem; background:var(--ll-panel); padding:1rem 1.1rem; margin:.75rem 0; }
.ll-panel-title { font-weight:750; margin-bottom:.3rem; }
.ll-panel p,.ll-risk-row p,.ll-priority p,.ll-ask-shell p { max-width:75ch; color:var(--ll-muted) !important; line-height:1.55; margin:.35rem 0; }
.ll-inline-meta { color:var(--ll-faint); font-size:.72rem; margin-top:.65rem; }
.ll-risk-row { padding:1.15rem; margin-top:1rem; border-bottom-left-radius:.25rem; border-bottom-right-radius:.25rem; }
.ll-risk-head { display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; }
.ll-risk-head h2 { margin:.2rem 0 .6rem; font-size:1.15rem; }
.ll-risk-index { color:var(--ll-accent); font-size:.72rem; font-weight:800; }
.ll-risk-clause { color:var(--ll-text) !important; font-weight:600; }
.ll-label { color:var(--ll-faint); font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; margin-top:.8rem; }
.ll-risk-meta { margin-top:.8rem; }
.ll-evidence { border:1px solid var(--ll-border); border-top:0; border-radius:.25rem .25rem .85rem .85rem; background:oklch(0.145 0.012 250); padding:.85rem 1rem; margin:0 0 1rem; }
.ll-evidence-head { display:flex; justify-content:space-between; gap:1rem; color:var(--ll-faint); font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
.ll-evidence blockquote { border:0; margin:.65rem 0 0; padding:0; color:var(--ll-muted); font-size:.9rem; line-height:1.5; }
.ll-priority { display:grid; grid-template-columns:2.2rem 1fr; gap:.8rem; }
.ll-priority-number { width:2rem; height:2rem; display:grid; place-items:center; border-radius:50%; background:var(--ll-accent-soft); color:var(--ll-accent); font-weight:800; }
.ll-priority h2,.ll-ask-shell h2,.ll-comparison-summary h2 { margin:0 0 .35rem; font-size:1.1rem; }
.ll-message { border:1px solid var(--ll-border); border-radius:.85rem; padding:.85rem 1rem; margin:.7rem 0; }
.ll-message-user { background:var(--ll-panel-soft); }
.ll-message-assistant { background:var(--ll-panel); }
.ll-message-label { color:var(--ll-faint); font-size:.68rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
.ll-message p { white-space:pre-wrap; line-height:1.55; margin:.35rem 0 0; }

/* Verify workspace: a dense reviewer desk for synthetic identity reconciliation. */
.ll-verify-header h1 { font-size:2.35rem; }
.ll-verify-summary { grid-template-columns:repeat(4,1fr); }
.ll-verify-brief { display:grid; grid-template-columns:1.25fr .75fr; gap:1px; overflow:hidden; border:1px solid var(--ll-border); border-radius:.85rem; background:var(--ll-border); margin:1.2rem 0 1.8rem; }
.ll-verify-brief > div { min-height:10rem; padding:1.25rem; background:var(--ll-panel); }
.ll-verify-brief > div:first-child { display:flex; flex-direction:column; justify-content:space-between; }
.ll-verify-brief p { max-width:68ch; margin:.8rem 0 0; color:var(--ll-muted) !important; font-size:1rem; line-height:1.6; }
.ll-verify-recommendation { display:flex; flex-direction:column; justify-content:space-between; }
.ll-verify-recommendation > span { color:var(--ll-faint); font-size:.7rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.ll-verify-recommendation > strong { margin:.5rem 0; font-size:1.8rem; letter-spacing:-.03em; }
.ll-verify-recommendation p { margin:0; font-size:.84rem; line-height:1.45; }
.ll-verify-finding { margin-bottom:0; }
.ll-evidence-panel { min-height:11rem; padding:1rem; border:1px solid var(--ll-border); border-radius:.8rem; background:var(--ll-panel); }
.ll-evidence-panel h3 { margin:.8rem 0 .35rem; font-size:1.05rem; line-height:1.35; word-break:break-word; }
.ll-evidence-panel p { margin:0; color:var(--ll-muted) !important; font-size:.78rem; }
.ll-audit-row { margin:.75rem 0; padding:1rem; border-top:1px solid var(--ll-border); border-bottom:1px solid var(--ll-border); }
.ll-audit-row > div:first-child { display:flex; align-items:center; gap:.75rem; }
.ll-audit-row p { max-width:70ch; margin:.7rem 0; color:var(--ll-muted) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap:.35rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { min-height:40px; padding:.35rem .5rem; border:1px solid var(--ll-border); border-radius:.6rem; background:var(--ll-panel); }

.stButton > button,.stDownloadButton > button,button[kind="secondary"],button[kind="primary"] { min-height:44px; border-radius:.65rem; border:1px solid var(--ll-border-strong); font-weight:700; transition:background-color 180ms cubic-bezier(.25,1,.5,1),border-color 180ms cubic-bezier(.25,1,.5,1),color 180ms cubic-bezier(.25,1,.5,1); }
.stButton > button:hover,.stDownloadButton > button:hover { border-color:var(--ll-accent); color:var(--ll-text); }
button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,[role="tab"]:focus-visible { outline:3px solid var(--ll-focus) !important; outline-offset:2px; }
[data-testid="stFileUploaderDropzone"] { border-color:var(--ll-border-strong); background:var(--ll-panel); border-radius:.75rem; }
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-baseweb="select"] > div { background:var(--ll-panel) !important; border-color:var(--ll-border) !important; color:var(--ll-text) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--ll-border); border-radius:.75rem; overflow:hidden; }

@media (max-width:900px) {
    .block-container { padding:1rem 1rem 3rem; }
    .ll-topbar { align-items:flex-start; padding:.5rem 0; }
    .ll-nav-right { display:none; }
    .ll-setup-header { padding:1.4rem 0 1rem; }
    .ll-setup-grid { grid-template-columns:1fr; gap:1.4rem; }
    .ll-setup-header h1 { font-size:3rem; }
    .ll-setup-outcome { padding:.95rem 0 0; border-left:0; border-top:1px solid var(--ll-border); }
    .st-key-review_setup [data-testid="stForm"] { padding:1.1rem; }
    .st-key-report_actions { margin:0 0 .6rem; }
    .ll-hero { padding:1.6rem 0 1rem; }
    .ll-hero h1 { font-size:3rem; }
    .ll-signal-row { grid-template-columns:1fr; }
    .ll-signal + .ll-signal { border-left:0; border-top:1px solid var(--ll-border); padding-left:0; }
    .ll-report-header { flex-direction:column; }
    .ll-report-header h1 { font-size:2rem; }
    .ll-summary-strip { grid-template-columns:repeat(2,1fr); }
    .ll-summary-strip > div + div { border-left:0; }
    .ll-summary-strip > div:nth-child(even) { border-left:1px solid var(--ll-border); }
    .ll-summary-strip > div:nth-child(n+3) { border-top:1px solid var(--ll-border); }
    .ll-risk-head { flex-direction:column; }
    .ll-verify-brief { grid-template-columns:1fr; }
    .ll-verify-summary { grid-template-columns:repeat(2,1fr); }
}

@media (max-width:640px) {
    .ll-setup-header h1 { font-size:2.45rem; }
    .st-key-review_setup { margin-top:.65rem; }
    .st-key-review_setup [data-testid="stForm"] { padding:.9rem; border-radius:.8rem; }
    .ll-hero h1 { font-size:2.45rem; }
    .ll-summary-strip { grid-template-columns:1fr; }
    .ll-summary-strip > div:nth-child(even) { border-left:0; }
    .ll-summary-strip > div:nth-child(n+2) { border-top:1px solid var(--ll-border); }
    .ll-evidence-head { flex-direction:column; gap:.2rem; }
    .ll-priority { grid-template-columns:1fr; }
    .ll-verify-summary { grid-template-columns:1fr; }
}

@media (prefers-reduced-motion:reduce) {
    *,*::before,*::after { scroll-behavior:auto !important; transition-duration:.01ms !important; animation-duration:.01ms !important; }
}
</style>
"""
