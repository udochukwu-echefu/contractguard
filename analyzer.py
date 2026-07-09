import os
import json
from pathlib import Path

from dotenv import load_dotenv

from prompts import CONTRACT_ANALYSIS_PROMPT, REWRITE_PROMPT, QA_PROMPT

load_dotenv(Path(__file__).with_name(".env"))


class ContractQAChain:
    """Small retrieval QA wrapper compatible with the app's existing invoke call."""

    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def invoke(self, inputs):
        from langchain_core.output_parsers import StrOutputParser

        user_input = inputs["input"]
        chat_history = inputs.get("chat_history", [])

        retrieval_query = user_input
        if chat_history:
            rewrite_chain = REWRITE_PROMPT | self.llm | StrOutputParser()
            retrieval_query = rewrite_chain.invoke({
                "input": user_input,
                "chat_history": chat_history,
            })

        docs = self.retriever.invoke(retrieval_query)
        context = "\n\n".join(doc.page_content for doc in docs)
        response = (QA_PROMPT | self.llm).invoke({
            "input": user_input,
            "chat_history": chat_history,
            "context": context,
        })

        return {"answer": response.content}


def get_llm():
    from langchain_openai import ChatOpenAI

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file before running the app.")

    return ChatOpenAI(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1
    )


def parse_document(file_path):
    """Loads a PDF or TXT file and returns its text content and chunked documents."""
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    if file_path.endswith('.pdf'):
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(file_path)
        documents = loader.load()
        full_text = "\n".join([doc.page_content for doc in documents])
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
        documents = [Document(page_content=full_text)]

    if not full_text.strip():
        return "", []

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    
    return full_text, chunks


def analyze_contract(text):
    """Runs the main contract analysis prompt and returns a structured JSON dict."""
    llm = get_llm()
    json_llm = llm.bind(response_format={"type": "json_object"})
    
    chain = CONTRACT_ANALYSIS_PROMPT | json_llm
    
    response = chain.invoke({"contract_text": text})
    
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        raise ValueError("The model returned invalid JSON. Please try the analysis again.")


def setup_qa_chain(chunks):
    """Sets up a conversational RAG chain with the document chunks."""
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    if not chunks:
        raise ValueError("No document text was available for Q&A.")

    llm = get_llm()
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    return ContractQAChain(llm, retriever)
