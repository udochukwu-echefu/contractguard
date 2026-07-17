# ContractGuard

ContractGuard is an evidence-led document intelligence workspace with two modes:

- **Contract Review** turns agreements into evidence-linked risks, negotiation priorities, obligations, deadlines, comparisons, and grounded Q&A.
- **Verify Onboarding** reconciles synthetic identity documents against an application, flags mismatches with deterministic rules, and supports explainable human decisions.

The Verify milestone currently uses fictional demonstration cases only. It is not a production identity-verification or KYC service.

ContractGuard is an evidence-linked Streamlit workspace for first-pass contract review. It helps users identify clauses that deserve attention, inspect supporting excerpts, prepare negotiation questions, extract obligations and deadlines, compare revisions, and create a concise handoff for qualified counsel.

> ContractGuard is for education and triage only. It does not provide legal advice.

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
- **Offline evaluation fixtures** for citation coverage, quote support, schema completeness, and expected-risk recall
- **PDF, DOCX, Markdown, CSV, and JSON exports**
- **Privacy notice and deletion controls** at the upload point
- **Responsive, keyboard-accessible dark interface**
- **Synthetic onboarding case queue** with low-, medium-, and high-risk examples
- **Deterministic identity reconciliation** for names, dates of birth, addresses, document expiry, extraction confidence, and simulated face-match status
- **Reviewer decision and audit history** with explainable recommendations and JSON case export

## Data handling

- Uploaded text is sent to the configured Groq model for analysis and Q&A generation.
- Embeddings are computed in the running app using `all-MiniLM-L6-v2`.
- Temporary upload files are deleted after parsing.
- Review reports and notes are stored in the configured database and scoped to the authenticated owner.
- Extracted source text is not stored unless the reviewer explicitly enables source retention before upload.
- Saved reviews are hard-deleted at the end of their selected retention period or when the reviewer deletes them.
- Verify currently processes bundled synthetic data only and does not accept real identity documents.
- Deployers should publish their own privacy, retention, subprocessors, logging, and security policies before accepting confidential production documents.

## Tech stack

- Streamlit 1.58
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
CONTRACTGUARD_AUTH_REQUIRED=true
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
- OIDC authenticates users but does not provide organisation roles by itself; production administrators must define their own membership and authorisation policy.
- Verify does not validate document authenticity against issuing authorities and does not perform production face matching or liveness detection.

## Production workspace setup

1. Provision a TLS-enabled Postgres database and add `DATABASE_URL` to Streamlit secrets or environment variables.
2. Configure Streamlit OIDC in `.streamlit/secrets.toml` or the Community Cloud secrets console, then set `CONTRACTGUARD_AUTH_REQUIRED=true`.
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
