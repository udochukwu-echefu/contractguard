APP_CSS = """
<style>
    @import url("https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800;900&display=swap");

    :root {
        --cg-ink: oklch(0.965 0 0);
        --cg-ink-soft: oklch(0.74 0 0);
        --cg-ink-faint: oklch(0.55 0 0);
        --cg-bg: oklch(0.135 0 0);
        --cg-bg-deep: oklch(0.105 0 0);
        --cg-panel: oklch(0.175 0 0);
        --cg-panel-2: oklch(0.215 0 0);
        --cg-line: oklch(0.305 0 0);
        --cg-line-soft: oklch(0.245 0 0);
        --cg-paper: oklch(0.93 0.01 90);
        --cg-paper-ink: oklch(0.22 0 0);
        --cg-accent: oklch(0.82 0.035 78);
        --cg-high: oklch(0.65 0.18 28);
        --cg-medium: oklch(0.78 0.12 78);
        --cg-low: oklch(0.67 0.13 145);
    }

    .stApp {
        background: var(--cg-bg-deep);
        color: var(--cg-ink);
        font-family: "Figtree", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp::before {
        content: none;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        opacity: 0.2;
    }

    [data-testid="stSidebar"] {
        background: var(--cg-bg);
        border-right: 1px solid var(--cg-line);
    }

    [data-testid="stSidebar"] * {
        color: var(--cg-ink);
    }

    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--cg-ink-faint) !important;
    }

    [data-testid="stSidebar"] label {
        color: var(--cg-ink-soft) !important;
        font-size: 0.78rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, p, li, label, button, input, textarea {
        font-family: "Figtree", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        letter-spacing: 0;
    }

    [data-testid="stAppViewContainer"] main,
    [data-testid="stAppViewContainer"] main p,
    [data-testid="stAppViewContainer"] main label,
    [data-testid="stAppViewContainer"] main li {
        color: var(--cg-ink);
    }

    .cg-shell {
        border: 1px solid var(--cg-line-soft);
        background: var(--cg-bg);
        border-radius: 18px;
        overflow: hidden;
    }

    .cg-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 0.95rem 1.05rem;
        border-bottom: 1px solid var(--cg-line-soft);
        background: var(--cg-bg);
    }

    .cg-nav-left, .cg-nav-right {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        flex-wrap: wrap;
    }

    .cg-dot {
        width: 0.66rem;
        height: 0.66rem;
        border-radius: 99px;
        background: var(--cg-ink-soft);
    }

    .cg-top-label {
        color: var(--cg-ink-soft);
        font-size: 0.78rem;
        font-weight: 720;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    .cg-chip {
        border: 1px solid var(--cg-line);
        border-radius: 999px;
        color: var(--cg-ink-soft);
        background: var(--cg-panel);
        padding: 0.38rem 0.68rem;
        font-size: 0.78rem;
        line-height: 1;
        white-space: nowrap;
    }

    .cg-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0.25rem 0 1.45rem;
    }

    .cg-mark {
        width: 2.65rem;
        height: 2.65rem;
        border-radius: 0.75rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: var(--cg-panel-2);
        color: var(--cg-ink);
        border: 1px solid var(--cg-line);
        font-weight: 900;
        font-size: 0.78rem;
        letter-spacing: -0.03em;
    }

    .cg-brand-text {
        font-size: 1.18rem;
        font-weight: 780;
        line-height: 1;
    }

    .cg-sidebar-copy {
        color: var(--cg-ink-soft) !important;
        line-height: 1.62;
        font-size: 0.95rem;
        margin-bottom: 1.25rem;
    }

    .cg-sidebar-note {
        margin: 1.15rem 0 1.35rem;
        padding: 0.95rem;
        border: 1px solid var(--cg-line);
        border-radius: 0.85rem;
        color: var(--cg-ink-soft);
        background: var(--cg-panel);
        font-size: 0.86rem;
        line-height: 1.55;
    }

    .cg-sidebar-rule {
        height: 1px;
        background: var(--cg-line-soft);
        margin: 1.25rem 0;
    }

    .cg-history-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin: 0 0 0.75rem;
    }

    .cg-history-title {
        color: var(--cg-ink);
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .cg-history-count {
        color: var(--cg-ink-faint);
        font-size: 0.82rem;
        line-height: 1.45;
        margin-top: 0.2rem;
    }

    .cg-history-card {
        border: 1px solid var(--cg-line-soft);
        border-radius: 0.95rem;
        background: var(--cg-panel);
        padding: 0.85rem;
        margin: 0.65rem 0 0.45rem;
    }

    .cg-history-card-active {
        border-color: var(--cg-accent);
        background: var(--cg-panel-2);
    }

    .cg-history-card-top {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 0.8rem;
        align-items: start;
        margin-bottom: 0.8rem;
    }

    .cg-history-name {
        color: var(--cg-ink);
        font-size: 0.92rem;
        font-weight: 780;
        line-height: 1.25;
    }

    .cg-history-source,
    .cg-history-date {
        color: var(--cg-ink-faint);
        font-size: 0.75rem;
        line-height: 1.35;
    }

    .cg-history-date {
        max-width: 5.6rem;
        text-align: right;
    }

    .cg-history-metrics {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }

    .cg-history-metric {
        display: inline-flex;
        align-items: center;
        min-height: 1.55rem;
        border: 1px solid var(--cg-line);
        border-radius: 999px;
        padding: 0 0.48rem;
        background: var(--cg-bg);
        color: var(--cg-ink-soft);
        font-size: 0.72rem;
        font-weight: 760;
        line-height: 1;
    }

    .cg-history-metric.high {
        color: var(--cg-high);
    }

    .cg-history-metric.medium {
        color: var(--cg-medium);
    }

    .cg-history-metric.low {
        color: var(--cg-low);
    }

    .cg-kicker {
        color: var(--cg-accent);
        font-size: 0.78rem;
        font-weight: 820;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .cg-stage {
        padding: clamp(1.25rem, 4vw, 3.5rem);
    }

    .cg-hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.04fr) minmax(320px, 0.76fr);
        gap: clamp(1.5rem, 4vw, 3.5rem);
        align-items: center;
    }

    .cg-hero h1 {
        color: var(--cg-ink);
        font-size: clamp(4.3rem, 8.2vw, 8.6rem);
        line-height: 0.86;
        letter-spacing: -0.075em;
        max-width: 920px;
        margin: 1rem 0 1.2rem;
    }

    .cg-hero-copy {
        color: var(--cg-ink-soft) !important;
        max-width: 64ch;
        font-size: 1.06rem;
        line-height: 1.72;
        margin: 0 0 1.65rem;
    }

    .cg-hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: center;
        margin-bottom: 2rem;
    }

    .cg-action-primary, .cg-action-secondary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 2.75rem;
        border-radius: 999px;
        padding: 0 1rem;
        font-weight: 760;
        font-size: 0.9rem;
    }

    .cg-action-primary {
        color: var(--cg-bg-deep);
        background: var(--cg-ink);
    }

    .cg-action-secondary {
        color: var(--cg-ink-soft);
        border: 1px solid var(--cg-line);
        background: var(--cg-panel);
    }

    .cg-signal-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        border: 1px solid var(--cg-line-soft);
        border-radius: 1rem;
        overflow: hidden;
        background: var(--cg-bg);
    }

    .cg-signal {
        min-height: 8.2rem;
        padding: 1rem;
        border-right: 1px solid var(--cg-line-soft);
    }

    .cg-signal:last-child {
        border-right: 0;
    }

    .cg-signal-code {
        color: var(--cg-accent);
        font-size: 0.78rem;
        font-weight: 850;
        letter-spacing: 0.11em;
        margin-bottom: 1.15rem;
    }

    .cg-signal-title {
        color: var(--cg-ink);
        font-weight: 780;
        margin-bottom: 0.38rem;
    }

    .cg-signal-copy {
        color: var(--cg-ink-faint) !important;
        line-height: 1.55;
        font-size: 0.9rem;
        margin: 0;
    }

    .cg-document {
        position: relative;
        border: 1px solid var(--cg-line);
        border-radius: 1.15rem;
        background: var(--cg-bg);
        padding: 0.8rem;
    }

    .cg-document::after {
        content: none;
    }

    .cg-document-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.55rem 0.8rem;
        color: var(--cg-ink-faint);
        font-size: 0.78rem;
    }

    .cg-paper {
        background: var(--cg-paper);
        color: var(--cg-paper-ink);
        border-radius: 0.75rem;
        min-height: 27rem;
        padding: 1.2rem;
        overflow: hidden;
    }

    .cg-paper-title {
        color: var(--cg-paper-ink);
        font-size: 0.9rem;
        font-weight: 850;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .cg-paper-line {
        height: 0.58rem;
        border-radius: 999px;
        background: oklch(0.78 0.02 95);
        margin-bottom: 0.7rem;
    }

    .cg-paper-line.short { width: 54%; }
    .cg-paper-line.medium { width: 76%; }

    .cg-finding {
        margin-top: 1.4rem;
        border: 1px solid oklch(0.66 0.1 28);
        border-radius: 0.65rem;
        background: oklch(0.9 0.025 35);
        padding: 0.8rem;
    }

    .cg-finding-label {
        color: oklch(0.44 0.12 28);
        font-size: 0.72rem;
        font-weight: 880;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }

    .cg-finding-copy {
        color: oklch(0.28 0.035 35) !important;
        line-height: 1.45;
        font-size: 0.9rem;
        margin: 0;
    }

    .cg-report-header {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 1.25rem;
        align-items: start;
        border: 1px solid var(--cg-line-soft);
        border-radius: 1.2rem;
        padding: clamp(1.25rem, 3vw, 2rem);
        background: var(--cg-panel);
        margin-bottom: 1rem;
        overflow: hidden;
    }

    .cg-report-header h1 {
        color: var(--cg-ink);
        margin: 0.7rem 0 0.75rem;
        font-size: clamp(2rem, 4.2vw, 3.6rem);
        line-height: 0.98;
        letter-spacing: -0.045em;
    }

    .cg-meta {
        color: var(--cg-ink-soft);
        font-size: 0.93rem;
        line-height: 1.55;
    }

    .cg-report-status {
        border-radius: 999px;
        border: 1px solid var(--cg-line);
        color: var(--cg-ink-soft);
        background: var(--cg-bg);
        font-weight: 760;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-size: 0.72rem;
        padding: 0.42rem 0.72rem;
        justify-self: end;
        white-space: nowrap;
    }

    .cg-summary-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 1rem 0 1.35rem;
    }

    .cg-stat {
        background: var(--cg-panel);
        border: 1px solid var(--cg-line-soft);
        border-radius: 0.9rem;
        padding: 1.1rem;
        min-height: 8rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .cg-stat-label {
        color: var(--cg-ink-faint);
        font-size: 0.75rem;
        font-weight: 760;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }

    .cg-stat-value {
        font-size: 3rem;
        line-height: 0.86;
        font-weight: 860;
        letter-spacing: -0.06em;
        color: var(--cg-ink);
    }

    .cg-stat-high .cg-stat-value { color: var(--cg-high); }
    .cg-stat-medium .cg-stat-value { color: var(--cg-medium); }
    .cg-stat-low .cg-stat-value { color: var(--cg-low); }

    .cg-panel {
        border: 1px solid var(--cg-line-soft);
        border-radius: 1rem;
        background: var(--cg-panel);
        padding: 1rem 1.05rem;
        margin-bottom: 0.75rem;
    }

    .cg-panel-title {
        color: var(--cg-ink);
        font-size: 0.98rem;
        font-weight: 760;
        margin-bottom: 0.35rem;
    }

    .cg-panel-copy {
        color: var(--cg-ink-soft) !important;
        line-height: 1.58;
        margin: 0;
    }

    .cg-risk-row {
        border: 1px solid var(--cg-line-soft);
        border-radius: 1rem;
        padding: 1rem;
        background: var(--cg-panel);
        margin-bottom: 0.8rem;
    }

    .cg-risk-head {
        display: grid;
        grid-template-columns: 2.4rem minmax(0, 1fr) auto;
        gap: 0.9rem;
        align-items: start;
        margin-bottom: 0.65rem;
    }

    .cg-risk-index {
        color: var(--cg-ink-faint);
        font-size: 0.8rem;
        font-weight: 820;
        letter-spacing: 0.08em;
        padding-top: 0.18rem;
    }

    .cg-risk-clause {
        color: var(--cg-ink);
        font-weight: 720;
        line-height: 1.45;
    }

    .cg-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 6.1rem;
        padding: 0.34rem 0.62rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 820;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        white-space: nowrap;
        border: 1px solid currentColor;
        background: var(--cg-bg);
    }

    .cg-pill-high { color: var(--cg-high); }
    .cg-pill-medium { color: var(--cg-medium); }
    .cg-pill-low { color: var(--cg-low); }

    .cg-label {
        margin: 0.85rem 0 0.32rem;
        font-size: 0.72rem;
        font-weight: 790;
        color: var(--cg-ink-faint);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .cg-ask-shell {
        border: 1px solid var(--cg-line-soft);
        border-radius: 1rem;
        padding: 1rem;
        background: var(--cg-panel);
        margin-bottom: 0.9rem;
    }

    .cg-ask-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .cg-ask-title {
        color: var(--cg-ink);
        font-size: 1.05rem;
        font-weight: 780;
        margin-top: 0.32rem;
    }

    .cg-ask-copy {
        color: var(--cg-ink-soft) !important;
        max-width: 68ch;
        margin: 0.42rem 0 0;
        line-height: 1.58;
    }

    .cg-prompt-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.65rem;
    }

    .cg-prompt {
        border: 1px solid var(--cg-line-soft);
        border-radius: 0.8rem;
        background: var(--cg-bg);
        color: var(--cg-ink-soft);
        font-size: 0.88rem;
        line-height: 1.45;
        padding: 0.8rem;
    }

    .cg-message {
        border: 1px solid var(--cg-line-soft);
        border-radius: 1rem;
        background: var(--cg-panel);
        padding: 0.95rem 1rem;
        margin-bottom: 0.7rem;
    }

    .cg-message-user {
        background: var(--cg-panel-2);
    }

    .cg-message-label {
        color: var(--cg-ink-faint);
        font-size: 0.72rem;
        font-weight: 790;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.42rem;
    }

    .cg-message-copy {
        color: var(--cg-ink-soft) !important;
        line-height: 1.62;
        margin: 0;
    }

    div[data-testid="stTabs"] {
        margin-top: 0.75rem;
    }

    div[data-testid="stTabs"] button {
        position: relative;
        border-radius: 0;
        min-height: 2.45rem;
        padding: 0 0.9rem;
        background: transparent !important;
    }

    div[data-testid="stTabs"] button p {
        color: var(--cg-ink-faint);
        font-weight: 650;
        font-size: 0.88rem;
    }

    div[data-testid="stTabs"] button[aria-selected="true"]::after {
        content: "";
        position: absolute;
        left: 0.9rem;
        right: 0.9rem;
        bottom: 0.1rem;
        height: 1px;
        background: var(--cg-accent);
    }

    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: var(--cg-ink);
        font-weight: 760;
    }

    [data-testid="stFileUploader"] section {
        min-height: 8.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.2rem !important;
        background: var(--cg-bg-deep) !important;
        border: 1px dashed var(--cg-line) !important;
        border-radius: 0.95rem !important;
    }

    [data-testid="stFileUploader"] section > div {
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        align-items: center;
        text-align: center;
    }

    [data-testid="stFileUploader"] svg {
        margin: 0 auto 0.35rem;
    }

    [data-testid="stTextArea"] textarea {
        background: var(--cg-panel) !important;
        color: var(--cg-ink) !important;
        border: 1px solid var(--cg-line-soft) !important;
        border-radius: 1rem !important;
        min-height: 7.5rem !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
        resize: vertical !important;
        box-shadow: none !important;
        caret-color: var(--cg-accent) !important;
    }

    [data-testid="stTextArea"] [data-baseweb="textarea"] {
        background: var(--cg-panel) !important;
        border: 1px solid var(--cg-line-soft) !important;
        border-radius: 1rem !important;
        box-shadow: none !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: var(--cg-ink-faint) !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextArea"] textarea:focus-visible,
    [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
        border-color: var(--cg-accent) !important;
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stForm"] {
        border: 1px solid var(--cg-line-soft) !important;
        border-radius: 1rem !important;
        background: var(--cg-bg) !important;
        padding: 1rem !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    button[kind],
    button[data-testid^="baseButton"] {
        border-radius: 999px;
        border: 1px solid var(--cg-line) !important;
        background: var(--cg-panel-2) !important;
        color: var(--cg-ink) !important;
        font-weight: 760;
        min-height: 2.75rem;
        transition: background-color 180ms ease-out, border-color 180ms ease-out, color 180ms ease-out;
        cursor: pointer;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stButton > button:focus,
    .stDownloadButton > button:focus,
    .stFormSubmitButton > button:focus,
    .stButton > button:active,
    .stDownloadButton > button:active,
    .stFormSubmitButton > button:active,
    button[kind]:hover,
    button[kind]:focus,
    button[kind]:active,
    button[data-testid^="baseButton"]:hover,
    button[data-testid^="baseButton"]:focus,
    button[data-testid^="baseButton"]:active {
        background: var(--cg-panel-2) !important;
        border-color: var(--cg-accent) !important;
        color: var(--cg-ink) !important;
        box-shadow: none !important;
    }

    .stButton > button:hover *,
    .stDownloadButton > button:hover *,
    .stFormSubmitButton > button:hover *,
    .stButton > button:focus *,
    .stDownloadButton > button:focus *,
    .stFormSubmitButton > button:focus *,
    .stButton > button:active *,
    .stDownloadButton > button:active *,
    .stFormSubmitButton > button:active *,
    button[kind]:hover *,
    button[kind]:focus *,
    button[kind]:active *,
    button[data-testid^="baseButton"]:hover *,
    button[data-testid^="baseButton"]:focus *,
    button[data-testid^="baseButton"]:active * {
        color: var(--cg-ink) !important;
    }

    .stAlert {
        border-radius: 0.95rem;
    }

    @media (max-width: 980px) {
        .cg-hero-grid, .cg-report-header {
            grid-template-columns: 1fr;
        }

        .cg-signal-row, .cg-summary-grid, .cg-prompt-grid {
            grid-template-columns: 1fr;
        }

        .cg-ask-header {
            flex-direction: column;
        }

        .cg-signal {
            border-right: 0;
            border-bottom: 1px solid var(--cg-line-soft);
        }

        .cg-signal:last-child {
            border-bottom: 0;
        }

        .cg-risk-head {
            grid-template-columns: 2rem minmax(0, 1fr);
        }

        .cg-risk-head .cg-pill {
            grid-column: 2;
            justify-self: start;
        }
    }
</style>
"""
