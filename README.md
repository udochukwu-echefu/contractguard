# ContractGuard

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
- **Session notes and review history**
- **PDF, DOCX, Markdown, CSV, and JSON exports**
- **Privacy notice and deletion controls** at the upload point
- **Responsive, keyboard-accessible dark interface**

## Data handling

- Uploaded text is sent to the configured Groq model for analysis and Q&A generation.
- Embeddings are computed in the running app using `all-MiniLM-L6-v2`.
- Temporary upload files are deleted after parsing.
- Review history and notes are stored in the active Streamlit session only.
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
- Session history is not a persistent multi-user workspace; production collaboration requires authentication and durable storage.
