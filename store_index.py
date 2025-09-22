from dotenv import load_dotenv
import os
from src.helper import extract_from_pdf, filter_to_minimal_docs, chunker, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# env
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# extract
extracted_data = extract_from_pdf(data="pdf-resumes/")

# filter
filter_data = filter_to_minimal_docs(extracted_data)

# chunk
text_chunks = chunker(filter_data)

# embed
embeddings = download_embeddings()

# pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "resume-search"

# create
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# index
index = pc.Index(index_name)

# store
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print(f"Indexed {len(text_chunks)} chunks into '{index_name}'")
