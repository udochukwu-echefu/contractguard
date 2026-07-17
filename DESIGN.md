# ContractGuard Design System

## Direction

A dark, editorial product workspace inspired by a careful document review desk. The visual system is restrained: near-black blue-tinted surfaces, warm off-white text, a coral action accent, and semantic risk colors. Typography is compact and utilitarian, with larger display type reserved for the empty state.

## Color

- Background: `oklch(0.13 0.008 250)`
- Raised surface: `oklch(0.17 0.01 250)`
- Soft surface: `oklch(0.20 0.012 250)`
- Border: `oklch(0.29 0.012 250)`
- Primary text: `oklch(0.94 0.008 80)`
- Muted text: `oklch(0.70 0.012 250)`
- Accent: `oklch(0.68 0.17 25)`
- High risk: `oklch(0.67 0.20 25)`
- Medium risk: `oklch(0.76 0.14 80)`
- Low risk / positive: `oklch(0.70 0.13 145)`

## Typography

Use Figtree for interface and display text with a system sans-serif fallback. Body copy is 0.95 to 1rem at 1.55 line height. Labels use 0.72 to 0.78rem uppercase text with moderate tracking. Long prose is capped near 70 characters.

## Layout

- Persistent 300px sidebar on desktop, collapsed by Streamlit on mobile
- Main content capped near 1180px
- Compact report summary strip, not oversized metric cards
- Sticky report navigation where platform behavior allows
- Single-column risk and evidence reading flow
- Responsive breakpoints at 900px and 640px

## Components

- Buttons: minimum 44px height, subtle full border, clear focus ring
- Findings: bordered rows with severity, evidence, impact, and action
- Evidence: quiet tinted block with source label and quoted excerpt
- Status pills: semantic color plus text, never color alone
- Empty states: short instructions and one clear next action
- Loading: staged status text for parsing, analysis, and retrieval setup
- Workspace switcher: two explicit product modes, Contract Review and Verify Onboarding
- Verify queue: applicant, risk score, flag count, and suggested action at a glance
- Reconciliation matrix: submitted and extracted values shown without hiding missing fields
- Evidence panels: source, exact value, field, location, and extraction confidence
- Decision history: recommendation, human decision, rationale, reviewer, and timestamp
- Review policy: playbook, retention period, and source-text choice grouped before upload
- Playbook result: preferred position, fallback, escalation trigger, owner, matched finding, and evidence
- Saved review history: owner-scoped records labelled as saved rather than session-only

## Motion

Use only 150 to 220ms state transitions with ease-out-quart. Respect `prefers-reduced-motion`. Do not animate layout properties.
