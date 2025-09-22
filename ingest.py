from dotenv import load_dotenv
import os
from src.helper import extract_from_pdf, filter_to_minimal_docs, chunker, download_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "resume-index"

# create index if not exists
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

docs = extract_from_pdf("resumes/")
filtered = filter_to_minimal_docs(docs)
chunks = chunker(filtered)
embeddings = download_embeddings()

PineconeVectorStore.from_documents(
    documents=chunks,
    index_name=index_name,
    embedding=embeddings
)

print(" Data ingested into Pinecone successfully!")
