# Lenslayer Design System

## Direction

A light, botanical product workspace inspired by a careful document review desk in daylight. The visual system uses mist green working surfaces, a forest navigation rail, leaf-green actions, and distinct semantic risk colors. Typography remains compact and utilitarian, with larger display type reserved for the empty state.

## Color

- Main canvas: `#FBFCF7`
- Mist secondary background: `#EDF1D6`
- Sage border and quiet emphasis: `#9DC08B`
- Leaf action and positive state: `#609966`
- Forest navigation and primary action: `#40513B`
- Primary text: `#263424`
- Muted text: `#52634F`
- High risk: `#A8453C`
- Medium risk: `#946515`
- Previous dark coral theme backup: `branding/theme-backups/2026-07-29-dark-coral/`

## Typography

Use Figtree for interface and display text with a system sans-serif fallback. Body copy is 0.95 to 1rem at 1.55 line height. Labels use 0.72 to 0.78rem uppercase text with moderate tracking. Long prose is capped near 70 characters.

## Layout

- Persistent 300px sidebar on desktop, collapsed by Streamlit on mobile
- Main content capped near 1180px
- New-review setup is a primary main-page workflow: upload, review context, policy, privacy, consent, then action
- Sidebar is secondary navigation only: account, current review controls, and saved review history
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
- Review entry: one prominent `Review contract` action, with the sample agreement as a secondary path
- Playbook result: preferred position, fallback, escalation trigger, owner, matched finding, and evidence
- Saved review history: owner-scoped records labelled as saved rather than session-only

## Motion

Use only 150 to 220ms state transitions with ease-out-quart. Respect `prefers-reduced-motion`. Do not animate layout properties.
