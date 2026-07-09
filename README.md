# ContractGuard

ContractGuard is a Streamlit app for first-pass contract review. It helps users identify risky clauses, missing protections, key terms, and legal jargon before they decide whether to ask for changes or get professional advice.

> ContractGuard is for education and triage only. It is not a substitute for a lawyer.

## Features
- **PDF and TXT upload**: Parses common contract formats
- **Structured review**: Extracts contract type, parties, key terms, risk assessment, missing protections, and jargon
- **Plain-English explanations**: Turns dense clauses into practical summaries
- **Document Q&A**: Uses retrieval-augmented generation so follow-up answers stay grounded in the uploaded contract
- **Sample lease**: Includes a built-in demo contract for quick testing

## Tech Stack
- **UI**: Streamlit
- **LLM**: Groq-hosted Llama model through LangChain's OpenAI-compatible adapter
- **Vector DB**: ChromaDB
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Document Loading**: PyPDFLoader

## Setup Instructions

1. Clone the repository
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root or this directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## How It Works
1. **Parse**: The uploaded contract is loaded from PDF or text.
2. **Analyze**: The full text is sent to the model with a JSON-only prompt for structured output.
3. **Display**: Streamlit renders the results across focused tabs for terms, risks, missing protections, jargon, and Q&A.
4. **Retrieve**: Contract chunks are embedded into a temporary Chroma collection for document-grounded follow-up questions.

## Limitations
- Scanned PDFs without selectable text may not parse correctly.
- The app can miss context, misclassify risk, or produce incomplete analysis.
- Legal decisions should be reviewed with a qualified professional.
