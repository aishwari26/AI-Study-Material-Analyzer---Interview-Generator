
# 📚 AI Study Material Analyzer & Interview Generator

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen.svg)](https://ai-study-material-analyzer---interview-generator-vsfbzkiqxgeuq.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-black.svg)](https://www.langchain.com/)

An intelligent GenAI application that processes study materials and automatically generates highly relevant, context-aware interview questions. Built to help students and professionals test their knowledge instantly based on their own notes, documents, or textbooks.

**Try the live app here:** [Launch AI Interview Generator](https://ai-study-material-analyzer---interview-generator-vsfbzkiqxgeuq.streamlit.app/)

---

## 🚀 Overview

Preparing for technical interviews or exams requires targeted practice. This tool eliminates the manual work of creating flashcards or practice tests. By leveraging **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** principles, the application analyzes uploaded text or documents and synthesizes intelligent, challenging questions tailored to the exact context of the provided material.

## ✨ Features

- **Context-Aware Question Generation:** Analyzes your specific study material to generate highly relevant interview questions.
- **Automated Document Parsing:** Extracts and processes raw text for immediate LLM analysis.
- **Interactive UI:** A clean, fast, and responsive user interface deployed via Streamlit Cloud.
- **Fast Execution:** Uses optimized prompting for rapid question generation.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend & Deployment:** Streamlit, Streamlit Cloud
- **AI / ML Frameworks:** LangChain, PyTorch
- **Core Logic:** Large Language Models (LLMs), Prompt Engineering

## ⚙️ Run Locally

Follow these steps to run the project on your own machine.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add your API key:

```env
LLM_API_KEY=your_api_key_here
```

Use the exact environment variable name expected by your application. Never upload your real API key or `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## 💡 How to Use

1. Open the [Live App](https://ai-study-material-analyzer---interview-generator-vsfbzkiqxgeuq.streamlit.app/).
2. Upload your study material, notes, or a supported document.
3. Let the application analyze the uploaded content.
4. Generate targeted interview or exam questions based on your material.
5. Use the generated questions to test your knowledge.

## 📬 Contact & Connect

**Aishwari Bambale**

- **LinkedIn:** https://www.linkedin.com/in/aishwari-bambale-6b4b81442/
- **GitHub:** https://github.com/aishwari26
