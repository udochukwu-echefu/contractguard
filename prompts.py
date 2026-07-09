from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CONTRACT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You review contracts for education and first-pass risk triage. You are not a lawyer and must not present your analysis as legal advice.

You must reply with ONLY a valid JSON object matching the following structure:
{{
  "contract_type": "string (e.g., Residential Lease, NDA, Employment Contract)",
  "parties_involved": ["string"],
  "key_terms": [
    {{"term": "string", "description": "string"}}
  ],
  "risk_assessment": [
    {{
      "clause": "string (the actual text or summary of the clause)",
      "risk_level": "High" | "Medium" | "Low",
      "explanation": "string (plain English explanation of why this is risky)",
      "recommendation": "string (what the user should ask to change)"
    }}
  ],
  "missing_protections": [
    {{"issue": "string", "explanation": "string (why this should be in the contract)"}}
  ],
  "jargon_decoder": [
    {{"term": "string", "plain_english": "string"}}
  ]
}}

Be specific, concise, and practical. Flag clauses that deserve professional review, but do not invent facts outside the document. Make sure your output is valid JSON so it can be parsed programmatically.
"""),
    ("human", "Please analyze this contract:\n\n{contract_text}")
])

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("human", "Given the above conversation, rephrase the latest question "
              "to be a standalone question that can be understood without "
              "the chat history. Do NOT answer it, just rephrase it. If it doesn't need rephrasing, just repeat it."),
])

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You answer contract questions for education and first-pass review. "
               "Answer the user's question about their contract using ONLY the context below. "
               "If the answer isn't in the context, say you don't know based on the document. "
               "Explain things in plain English and recommend legal review for decisions with legal consequences.\n\n"
               "Context:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])
