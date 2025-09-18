# IMPORT NECESSARY LIBRARIES
from langchain_community.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


# extract text from the pdf file

def extract_from_pdf(file_path):
    loader = DirectoryLoader(file_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents
     
# RETURN ONLY MINIMAL DOCUMENTS WITH SOURCE AND CONTENT

def filter_to_minimal_docs(docs) :
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs



# Chunking the documents into smaller pieces

def chunker(docs ,chunk_size=1200 , chunk_oerlap= 100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_oerlap
    )
    text_chunks= text_splitter.split_documents(docs)

    return text_chunks

# WE USE THE SENTENCE TRANFORMERS EMBEDDING MODEL
 
def download_embeddings():
    """
    Download and return the HuggingFace embeddings model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings

embedding = download_embeddings()