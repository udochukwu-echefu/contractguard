# ContractGuard Design System

## Direction

ContractGuard is a careful review instrument, not an AI dashboard. The interface should feel calm, evidence-led, and suitable for an informed professional preparing a decision or counsel handoff. Structure comes from alignment, whitespace, and dividers. Cards are reserved for findings and document objects.

## Color

- Background: `#17191d`
- Primary surface: `#1e2126`
- Raised control surface: `#252930`
- Border: `#343941`
- Strong border: `#4a505a`
- Primary text: `#f1eee9`
- Muted text: `#abaeb5`
- Warm action accent: `#d87967`
- High: `#ef756e`
- Medium: `#d5a74d`
- Low: `#6db889`
- Needs verification: `#68a9d8`

Use the warm accent for primary actions and focus. Semantic colors are reserved for real states and always paired with text.

## Typography

Use Inter or the platform system UI stack. Body text is at least 16px on mobile with comfortable line height. Headings use a compact product scale, never marketing-display scale. Sentence case is standard. Uppercase and wide tracking are not used for routine labels.

## Information architecture

The report has three primary areas:

1. Review: Summary, Findings, Missing protections, Obligations and dates
2. Actions: Reviewer decisions, Negotiation plan, Ask the document
3. Tools: Compare versions, Export and handoff

The default path is explicit: Summary → Highest-risk findings → Decisions required → Negotiation plan → Handoff. Source-dependent tools are omitted from active navigation when unavailable and shown with a lock explanation and a new-review action.

## Layout and responsiveness

- Desktop sidebar contains account context, review history, and workspace settings.
- Mobile review history uses Streamlit's sidebar drawer.
- Main content is capped at 1160px.
- Findings use one full-width reading column; internal details can use three columns on desktop.
- At widths below 768px, finding details become a single column, controls become full width, the three-area segmented control remains scroll-safe, and safe-area bottom padding is applied.
- Controls and interactive help targets are at least 44×44px.
- No floating control may visually overlap review content.

## Core components

- Upload: one styled drop zone with format and size guidance, selected-file state, native remove action, and parsing status.
- Context: perspective, goal, jurisdiction, and risk posture each include a short consequence explanation.
- Report header: title, category, parties, source, governing law, classification confidence, synopsis, and persistent legal-advice disclosure.
- Finding: severity, specific title, clause summary, why it matters, consequence, reviewer action, semantic category, confidence explanation, jurisdiction state, recommendation scope, human state, source excerpt, citation, and optional replacement language.
- Human decisions: No decision, Accept, Reject, Needs counsel, or Resolved, with owner and note.
- Audit: decision history and audit events are secondary expanders.
- Export: PDF is primary; DOCX, Markdown, obligations CSV, deadlines CSV, and JSON live under Export options with use descriptions.
- Destructive actions: red, inside Workspace settings, named confirmation required, and recovery status stated.

## Trust rules

- Contract classification happens before specialist playbook selection.
- Contract category and playbook must agree.
- Semantic playbook matching uses controlled finding categories and clause evidence, never generated recommendations.
- Unknown jurisdiction forces general negotiation language and an enforceability check.
- Confidence describes evidence and model certainty, not legal correctness.
- AI findings and human decisions remain visibly distinct.

## Streamlit containment

Keep only the native header space required for sidebar open and close controls. Hide toolbar actions, status controls, heading anchors, and unnecessary dataframe toolbars. Custom CSS removes default uploader ornament while preserving accessible native upload behavior.
