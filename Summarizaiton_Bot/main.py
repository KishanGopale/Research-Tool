import os
import streamlit as st
import time
import google.generativeai as genai

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS

GOOGLE_API_KEY = "your api key"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("News Research Tool")
st.sidebar.title("News Article URLs")

### 🔥 CHANGED: Removed pickle file usage, replaced with FAISS local storage
faiss_path = "faiss_index"

# Sidebar input for URLs
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_urls_clicked = st.sidebar.button("Process URLs")
main_placeholder = st.empty()

# When button is clicked
if process_urls_clicked:
    # Load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data loading started...")
    data = loader.load()

    # Split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text splitting started...")
    docs = text_splitter.split_documents(data)

    # Embedding + FAISS
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        transport="grpc"  # forces sync mode, avoids async event loop
    )
    vectorstore = FAISS.from_documents(docs, embedding)
    main_placeholder.text("Building FAISS index...")
    time.sleep(2)

    ### 🔥 CHANGED: Save vectorstore locally instead of pickle
    vectorstore.save_local(faiss_path)


# Query Section
query = main_placeholder.text_input("Question: ")

if query:
    ### 🔥 CHANGED: Load FAISS index properly with embedding
    if os.path.exists(faiss_path):
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            transport="grpc" 
        )
        vectorstore = FAISS.load_local(faiss_path, embedding, allow_dangerous_deserialization=True)

        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # 🔥 Added missing llm
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever()
        )

        result = chain({"question": query}, return_only_outputs=True)

        # Display result
        st.header("Answer")
        st.write(result["answer"])

        # Display sources
        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")
            for source in sources_list:
                st.write(source)
