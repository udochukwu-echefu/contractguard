# Lenslayer

Lenslayer is an evidence-led document intelligence workspace with two modes:

- **Contract Review** turns agreements into evidence-linked risks, negotiation priorities, obligations, deadlines, comparisons, and grounded Q&A.
- **Verify Onboarding** reconciles synthetic identity documents against an application, flags mismatches with deterministic rules, and supports explainable human decisions.

The Verify milestone currently uses fictional demonstration cases only. It is not a production identity-verification or KYC service.

Lenslayer is an evidence-linked Streamlit workspace for first-pass contract review. It helps users identify clauses that deserve attention, inspect supporting excerpts, prepare negotiation questions, extract obligations and deadlines, compare revisions, and create a concise handoff for qualified counsel.

## Platform migration

Milestone 1 provides the platform foundation in `backend/`: extracted analysis logic, FastAPI, production-enforced PostgreSQL, a database-backed worker, production-enforced private S3-compatible storage, OIDC authentication, organisations and roles, permissions, audit events, and in-product notification infrastructure. SQLite, local identity, and filesystem storage remain development-only conveniences.

Milestone 2 provides the dashboard MVP in `dashboard/`: Today, Inbox, a searchable and filterable contract repository, the new-contract workflow, permanent contract pages, processing and error states, mobile navigation, and editable workspace defaults. The browser connects to FastAPI through a server-side Next.js proxy, keeping API configuration and identity credentials out of client bundles.

Milestone 3 provides review intelligence in the dashboard: executive summaries, evidence-linked risks and possible protection gaps, retained-document Q&A, obligations, payments, deadlines, negotiation priorities, suggested wording, baseline playbook evaluation, extraction warnings, deletion and retention controls, and PDF, DOCX, CSV, Markdown, and JSON exports.

Milestone 4 adds the contract-operations and collaboration layer: comments and mentions, attributable accept/change/escalate/resolve decisions, conditional approval requests, reviewer-created actions, assignees, priorities, due dates, completion states, a contract activity feed, complete audit history, notification delivery, secure expiring external reviews, and structured counsel handoffs. AI findings never become tasks, decisions, or approvals automatically; a workspace member must record every material action.

Milestone 5 adds the post-signature operating layer and migrates Lenslayer Verify into the authenticated platform. Contract lifecycle records cover renewals, notice periods, obligations, payment reminders, post-signature tasks, recurring schedules, overdue escalation, a unified calendar with ICS export, and portfolio-wide evidence retrieval. Verify provides organization-scoped synthetic case queues, persisted reconciliation evidence, explainable discrepancy scoring, separate extraction-confidence signals, role-aware access, and append-only approve/escalate/reject decisions with reviewer rationale and audit history. Real identity-document upload remains intentionally disabled.

Milestone 6 adds the negotiation closeout layer: revised-document uploads, persistent version history, deterministic before-and-after comparison, negotiation checklist tracking, counterparty responses, accepted and rejected change records, unresolved point registers, and a final negotiation summary.

Milestone 7 adds the intake and integrations MVP: shared integration connection records, import provenance, forwarding-email intake, Google Drive file import, Slack notification connection metadata, organization API keys, public contract upload/read endpoints, webhook subscriptions, and durable webhook delivery logs. OneDrive, SharePoint, Dropbox, Telegram, WhatsApp secure links, and live provider OAuth adapters are planned follow-ons that can attach to the same import pipeline.

The reporting and governance layer adds time-range operational snapshots, contract throughput, action completion and current attention queues, Verify decision outcomes and overrides, reviewer workload, recent attributable activity, and downloadable CSV reports. Reports are derived from retained organization-scoped records and remain read-only for every workspace role.

See `backend/README.md` and `dashboard/README.md` for the local API, worker, and dashboard workflow.

For a free Cloudflare-first beta, see `docs/deployment/cloudflare-beta.md`. The dashboard is prepared for Cloudflare Workers through OpenNext, document storage can use Cloudflare R2, and the Python API/worker can run as containers behind Cloudflare DNS while avoiding a backend rewrite.

> Lenslayer is for education and triage only. It does not provide legal advice.

## Features

- **PDF, DOCX, and TXT ingestion** with automatic scanned-PDF OCR and extraction diagnostics
- **Review context** for party role, jurisdiction, goal, and risk posture
- **Evidence-linked findings** with location, verbatim excerpt, and confidence
- **Negotiation plan** with priority asks, fallbacks, and example replacement language
- **Possible protection gaps** phrased as items to verify, not confirmed omissions
- **Obligation, payment, deadline, and notice extraction**
- **Grounded Q&A** with inspectable retrieved sources
- **Version comparison** for substantive additions, removals, and risk changes
- **Persistent, owner-scoped review history** with configurable retention and hard deletion
- **Privacy-first source retention**: save the report while keeping source text opt-in
- **Reusable review playbooks** with preferred positions, fallbacks, escalation triggers, and owners
- **Human decision and audit history** for accept, change, escalate, and resolve workflows
- **Comments and mentions** with attributable discussion and in-product notifications
- **Approval requests and conditional approval rules** with recorded outcomes and reasoning
- **Secure external sharing** through expiring, revocable, read-only review links
- **Counsel handoff packages** with evidence, open risks, actions, decisions, and approvals
- **Contract operations** with assigned actions, priorities, due dates, completion states, overdue queues, and a responsive calendar
- **Lifecycle tracking** for renewals, notice periods, obligations, payments, and post-signature tasks
- **Recurring reminders and overdue escalation** with unified ICS calendar export
- **Cross-contract questions and portfolio search** with cited agreement excerpts
- **Evidence-to-action handoff** from contract risks, obligations, and deadlines, always initiated by a reviewer
- **Negotiation closeout** with revised-document versions, before-and-after comparison, counterparty responses, accepted/rejected changes, unresolved points, and final summaries
- **Provider-complete intake surface** for forwarding email, Google Drive, OneDrive, SharePoint, Dropbox, Slack, Telegram, WhatsApp secure links, API keys, public endpoints, webhooks, and delivery logs
- **Offline evaluation fixtures** for citation coverage, quote support, schema completeness, and expected-risk recall
- **PDF, DOCX, Markdown, CSV, and JSON exports**
- **Privacy notice and deletion controls** at the upload point
- **Responsive, keyboard-accessible dark interface**
- **Persistent onboarding case queue** for synthetic and real cases, with assignments, priorities, due dates, and controlled workflow states
- **Deterministic identity reconciliation** for names, dates of birth, addresses, document expiry, extraction confidence, and simulated face-match status
- **Secure onboarding-document pipeline** with private randomized object keys, hashes, retention dates, scan/extraction states, and expiring upload links
- **Evidence reconciliation, reviewer decision, and compliance audit history** with explainable recommendations, conflict-gated approval, real identities, and append-only records
- **Platform Verify dashboard** with persisted cases, document status, field reconciliation, assignment history, human decision ownership, overrides, and attributable history
- **Operational reports** with range filters, contract and task throughput, Verify outcomes, reviewer workload, governance activity, and CSV export

## Data handling

- Uploaded text is sent to the configured Groq model for analysis and Q&A generation.
- Embeddings are computed in the running app using `all-MiniLM-L6-v2`.
- Temporary upload files are deleted after parsing.
- Review reports and notes are stored in the configured database and scoped to the authenticated owner.
- Extracted source text is not stored unless the reviewer explicitly enables source retention before upload.
- Saved reviews are hard-deleted at the end of their selected retention period or when the reviewer deletes them.
- Verify accepts private onboarding documents and keeps synthetic fixtures clearly labelled. Issuer authenticity checks, malware scanning, liveness, and biometric matching require separately configured production services.
- Deployers should publish their own privacy, retention, subprocessors, logging, and security policies before accepting confidential production documents.

## Tech stack

- Streamlit 1.58
- Next.js 16, React 19, TypeScript, and TanStack Query for the product dashboard
- FastAPI, SQLAlchemy, Alembic, and a database-backed worker for the platform service
- Groq-hosted Llama through LangChain's OpenAI-compatible client
- ChromaDB and HuggingFace embeddings for retrieval
- PyPDF, python-docx, ReportLab

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_key_here
# Optional production Postgres connection. Local development defaults to SQLite.
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
# Require Streamlit OIDC before the app opens.
LENSLAYER_AUTH_REQUIRED=true
```

Run:

```bash
streamlit run app.py
```

The embedding model is cached once per app process. The first Q&A setup in a fresh deployment can take longer while model weights are downloaded.

## Known limitations

- OCR output can misread names, dates, signatures, and amounts and must be checked against the scan.
- Model-generated findings and suggested wording can be incomplete or wrong.
- A low attention score does not establish that an agreement is safe or enforceable.
- Citations should be checked against the original document.
- Local development uses a single labelled `local-demo` owner and SQLite. Do not expose that mode as a shared production workspace.
- OIDC supplies verified identity; Lenslayer's organization membership records provide the separate authorization boundary.
- Verify does not validate document authenticity against issuing authorities and does not perform production face matching or liveness detection.
- Reports are live snapshots of retained records. Deleted and expired records are intentionally excluded and the report is not a substitute for legal, compliance, or financial assurance.

## Production workspace setup

1. Provision a TLS-enabled Postgres database and add `DATABASE_URL` to Streamlit secrets or environment variables.
2. Configure Streamlit OIDC in `.streamlit/secrets.toml` or the Community Cloud secrets console, then set `LENSLAYER_AUTH_REQUIRED=true`.
3. Register the deployed app's `/oauth2callback` URL with the identity provider.
4. Confirm retention, database backups, encryption, subprocessors, and incident procedures before accepting confidential documents.

Example OIDC structure (replace every value in the deployment secrets console; never commit the real file):

```toml
[auth]
redirect_uri = "https://your-app.example.com/oauth2callback"
cookie_secret = "replace-with-a-strong-random-secret"
client_id = "provider-client-id"
client_secret = "provider-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

## Evaluation gate

Run the deterministic synthetic fixture suite before changing prompts or models:

```bash
python -m evaluation evaluation_fixtures
```

The command fails when citation coverage, source-quote support, schema completeness, expected-risk recall, or attention accuracy falls below the declared thresholds.
