import streamlit as st
from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel, Field




# Pull the key directly from the Streamlit Secrets dashboard
groq_api_key = st.secrets["GROQ_API_KEY"]

# Feed it explicitly into the LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"  
)

# --- PYDANTIC SCHEMAS FOR PHASE 2 ---
class MCQ(BaseModel):
    question: str = Field(description="The multiple choice question based on the text")
    option_a: str = Field(description="Option A")
    option_b: str = Field(description="Option B")
    option_c: str = Field(description="Option C")
    option_d: str = Field(description="Option D")
    answer: str = Field(description="The correct option letter (A, B, C, or D)")

class InterviewQuestion(BaseModel):
    question: str = Field(description="A challenging interview question based on the text")
    ideal_answer: str = Field(description="A brief ideal answer to evaluate the user")

class Assessment(BaseModel):
    mcqs: list[MCQ] = Field(description="A list of 3 multiple choice questions")
    interview_questions: list[InterviewQuestion] = Field(description="A list of 3 interview questions")

# --- APP CONFIG ---
st.set_page_config(page_title="AI Study Material Analyzer", layout="wide")
st.title("📚 AI Study Material Analyzer & Interview Generator")
st.caption("Transform dense PDFs into summaries, quizzes, and grounded Q&A.")

# Sidebar
st.sidebar.header("Document Upload")
uploaded_file = st.sidebar.file_uploader("Upload your PDF notes", type=["pdf"])

def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if uploaded_file:
    st.sidebar.success("PDF uploaded successfully!")
    with st.spinner("Reading PDF contents..."):
        raw_text = extract_pdf_text(uploaded_file)
        
    # --- FIXED GROQ MODEL HERE ---
    llm = ChatGroq(
        model="openai/gpt-oss-20b", 
        temperature=0.3,
        api_key="Paste your gsk_ key here"  # <--- Paste your gsk_ key here
    )
    
    # --- RAG VECTOR STORE CREATION ---
    with st.spinner("Indexing PDF into Vector Database for Q&A..."):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.create_documents([raw_text])
        embeddings = get_embedding_model()
        vectorstore = Chroma.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # --- UI TABS ---
    tab1, tab2, tab3 = st.tabs(["📝 Summary & Concepts", "🎯 Quiz & Interview Prep", "💬 Ask Document Q&A"])
    
    with tab1:
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Analyzing document..."):
                prompt = PromptTemplate(
                    input_variables=["text"],
                    template="Analyze the following text and provide a 3-bullet summary and 3 key concepts.\n\nText:\n{text}"
                )
                formatted_prompt = prompt.format(text=raw_text[:10000])
                response = llm.invoke(formatted_prompt)
                st.markdown(response.content)
                
    with tab2:
        if st.button("Generate Assessment (MCQs & Qs)", type="primary"):
            with st.spinner("Generating structured quiz..."):
                structured_llm = llm.with_structured_output(Assessment)
                assessment_data = structured_llm.invoke(
                    f"Create an assessment based on this text:\n\n{raw_text[:10000]}"
                )
                
                st.subheader("🗣️ Interview Questions")
                for i, q in enumerate(assessment_data.interview_questions):
                    with st.expander(f"Q{i+1}: {q.question}"):
                        st.success(f"**Ideal Answer:** {q.ideal_answer}")
                        
                st.subheader("📝 Multiple Choice Quiz")
                for i, mcq in enumerate(assessment_data.mcqs):
                    st.markdown(f"**{i+1}. {mcq.question}**")
                    st.write(f"A) {mcq.option_a}")
                    st.write(f"B) {mcq.option_b}")
                    st.write(f"C) {mcq.option_c}")
                    st.write(f"D) {mcq.option_d}")
                    st.caption(f"Correct Answer: {mcq.answer}")
                    st.divider()

    with tab3:
        st.subheader("💬 Ask Any Question About Your PDF")
        user_query = st.text_input("Type your question here:")
        
        if user_query:
            with st.spinner("Searching vector database & generating answer..."):
                relevant_docs = retriever.invoke(user_query)
                context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                rag_prompt = f"""
                You are a helpful assistant. Answer the question using ONLY the context provided below.
                If the answer is not in the context, say "I cannot find this in the document."

                Context from Document:
                {context_text}

                Question: {user_query}
                """
                
                answer = llm.invoke(rag_prompt)
                
                st.markdown("### 💡 Answer")
                st.write(answer.content)
                
                st.markdown("---")
                with st.expander("📌 View Retrieved Source Context (RAG Inspection)"):
                    for idx, doc in enumerate(relevant_docs):
                        st.markdown(f"**Chunk {idx+1}:**")
                        st.info(doc.page_content)

else:
    st.info("👈 Please upload a PDF file from the sidebar to begin.")
