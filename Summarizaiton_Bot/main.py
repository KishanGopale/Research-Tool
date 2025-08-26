import os
import streamlit as st
import pickle
from dotenv import load_dotenv

import google.generativeai as genai
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS


# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("📰 News Research Tool")

st.sidebar.title("News Article URLs")
file_path = "faiss_store_gemini.pkl"

# Sidebar URL inputs
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

# Process button
process_urls_clicked = st.sidebar.button("Process URLs")

main_placeholder = st.empty()

if process_urls_clicked:
    # Load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("🔄 Loading data from URLs...")
    data = loader.load()

    # Split data into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("✂️ Splitting text into chunks...")
    docs = text_splitter.split_documents(data)

    # Create embeddings
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        transport="grpc"  # ensures sync mode
    )

    main_placeholder.text("⚡ Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embedding)

    # Save FAISS index
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)

    main_placeholder.success("✅ Processing completed! You can now ask questions.")


# Input for question
query = st.text_input("💡 Ask a question about the articles:")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)

        # Define LLM (Google Gemini Pro)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

        # Create Retrieval-based QA chain
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever()
        )

        result = chain({"question": query}, return_only_outputs=True)

        # Show answer
        st.header("Answer")
        st.write(result["answer"])

        # Show sources
        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                st.write(source)
