# Research-Tool
A Streamlit app that summarizes up to 3 articles from URLs and answers user questions with Google Gemini + LangChain + FAISS.

# 📰 News Research Tool

A **Streamlit-powered research assistant** that lets you input up to **3 news article URLs** and then:  
- Summarizes the articles into embeddings  
- Allows you to ask **questions in natural language**  
- Provides **concise answers with sources** using **Google Gemini + LangChain + FAISS**

This tool is perfect for quickly extracting insights from multiple news articles and asking follow-up questions.

---

## ⚙️ Features
- Load and process news articles directly from URLs  
- Chunk and embed text with **Google Generative AI embeddings**  
- Store and retrieve vectors using **FAISS**  
- Answer user questions with **Google Gemini (LangChain QA)**  
- Cite sources for transparency  

---

## 📸 Demo
👉 Enter up to **3 news URLs** in the sidebar  
👉 Click **Process URLs** to load, split, and index the content  
👉 Ask any **question** in the input box  
👉 Get an **AI-generated answer** along with **sources** 🚀

<img width="1919" height="839" alt="Screenshot 2025-08-26 232956" src="https://github.com/user-attachments/assets/d716cd8f-b113-46e3-9a78-30d80de9c7e0" />
<img width="1919" height="864" alt="Screenshot 2025-08-26 232706" src="https://github.com/user-attachments/assets/1597c2eb-5e31-4f49-a228-95df515e383a" />

---

## 🛠️ Tech Stack
- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) - UI framework  
- [LangChain](https://www.langchain.com/) - Orchestration and QA chain  
- [Google Gemini API](https://ai.google.dev/) - LLM and embeddings  
- [FAISS](https://github.com/facebookresearch/faiss) - Vector store for similarity search  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/news-research-tool.git
cd news-research-tool
