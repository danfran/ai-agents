import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = None


def parse_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents[0]

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # Split the documents into chunks
    chunked_documents = text_splitter.split_documents(documents)
    return chunked_documents

# preload docs
def init_vector_store():
    directory_path = os.getenv('BASE_DOCUMENTS')

    docs = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            print(f"Loading file: {filename}")
            parsed_file = parse_pdf(os.path.join(directory_path, filename))
            docs.append(parsed_file)

    chunked_documents = split_documents(docs)

    embeddings_gg = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    global vector_store
    vector_store = InMemoryVectorStore(embeddings_gg)

    vector_store.add_documents(chunked_documents)
    retriever = vector_store.as_retriever(
        search_type='similarity',
        search_kwargs={'k': 5},
    )

    return retriever

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve the full CV related to a candidate."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}"
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
