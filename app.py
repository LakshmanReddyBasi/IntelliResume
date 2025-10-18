# app.py
from flask import Flask, render_template, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults  # ✅ Correct import
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from src.prompt import system_prompt
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate environment variables
if not PINECONE_API_KEY:
    raise ValueError(" PINECONE_API_KEY not set in .env")
if not GEMINI_API_KEY:
    raise ValueError(" GEMINI_API_KEY not set in .env")
if not TAVILY_API_KEY:
    raise ValueError(" TAVILY_API_KEY not set in .env")

# Set environment variables for LangChain
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

# Initialize embeddings and vector store
print(" Loading embeddings...")
embeddings = download_embeddings()

index_name = "resume-index"
print(f" Connecting to Pinecone index: {index_name}")
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize LLM — use real model name
print(" Initializing Gemini LLM...")
chat_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0.3
)

# Create RAG chain
print("⛓️  Building RAG chain...")
prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{input}")]
)
qa_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# Initialize Tavily Search Tool 
print("🔍 Setting up web search fallback...")
search_tool = TavilySearchResults(
    name="Web Search",
    description="Search the web when resume data is insufficient",
    max_results=3,
    search_depth="basic"
)

# Initialize agent
agent = initialize_agent(
    tools=[search_tool],
    llm=chat_model,
    agent="zero-shot-react-description",
    verbose=False,
    handle_parsing_errors=True 
)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print(f"\n💬 User Query: {msg}")

    try:
        # Step 1: Query resume database
        response = rag_chain.invoke({"input": msg})
        answer = response.get("answer", "").strip()

        print(f"📄 Resume Answer: {answer[:100]}...")

        # Step 2: Fallback to web if answer is empty or indicates lack of knowledge
        if not answer or any(phrase in answer.lower() for phrase in [
            "don't know", "not found", "not mentioned", "couldn't find",
            "no information", "unable to answer", "not in the context"
        ]):
            print("🌐 Fallback: Searching web...")
            try:
                web_result = agent.run(msg)
                reply = "🔍 Not found in resumes. Web result: " + web_result
            except Exception as e:
                reply = f"🔍 Not found in resumes. Web search failed: {str(e)}"
        else:
            reply = answer

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    print(f"💬 Bot Reply: {reply[:100]}...")
    return str(reply)

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host="0.0.0.0", port=8080, debug=True)
