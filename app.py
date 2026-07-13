import os
import time
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from config import CONFIG
from database import DatabaseManager
from vector_store import AdvancedRAGPipeline

# --- 1. CORE SUBSYSTEM INITIALIZATION ---
# Removed the LLM from caching so we can dynamically pass temperature without .bind() bugs
@st.cache_resource
def get_backend_infrastructure():
    db = DatabaseManager()
    rag = AdvancedRAGPipeline(db_manager=db)
    return db, rag

db_service, rag_service = get_backend_infrastructure()

# --- 2. GLOBAL SYSTEM PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI PDF Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. SESSION VARIABLE HYDRATION ---
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "theme" not in st.session_state: st.session_state.theme = "Dark"
if "total_chunks" not in st.session_state: st.session_state.total_chunks = rag_service.get_total_chunks()
if "stats" not in st.session_state: st.session_state.stats = db_service.get_statistics()

# --- 4. HIGH-SPECIFICITY UI CSS ENGINE ---
def inject_theme_engine(theme: str):
    """Overrides Streamlit UI elements. Fixed contrast issues for Light Theme."""
    if theme == "Light":
        style_payload = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600&display=swap');
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
            background-color: #F8FAFC !important; color: #0F172A !important; font-family: 'Inter', sans-serif; 
        }
        [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] { 
            background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; 
        }
        p, h1, h2, h3, span, label, [data-testid="stWidgetLabel"] p, .stMarkdown div p { 
            color: #0F172A !important; 
        }
        
        /* --- VISIBILITY FIX: Chat Input --- */
        [data-testid="stBottomBlockContainer"], [data-testid="stBottom"], div[class*="stChatInput"] { 
            background-color: #F8FAFC !important; 
        }
        [data-testid="stChatInput"] { background-color: transparent !important; }
        
        /* Force text and placeholder to be dark */
        [data-testid="stChatInput"] textarea { 
            background-color: #FFFFFF !important; 
            color: #0F172A !important; 
            -webkit-text-fill-color: #0F172A !important;
            caret-color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }
        [data-testid="stChatInput"] textarea::placeholder { 
            color: #64748B !important; 
            -webkit-text-fill-color: #64748B !important;
        }
        [data-testid="stChatInput"] textarea:focus { border: 1px solid #2563EB !important; }
        
        /* Send button icon */
        [data-testid="stChatInput"] button svg { fill: #0F172A !important; color: #0F172A !important; }
        
        /* File Uploader */
        [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploadDropzone"], section.stFileUploaderDropzone { 
            background-color: #F1F5F9 !important; border: 2px dashed #CBD5E1 !important; 
        }
        [data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploadDropzone"] * { 
            color: #0F172A !important; fill: #0F172A !important; 
        }
        
        /* Standard Buttons */
        .stButton>button, div[data-testid="stFileUploader"] button { 
            background-color: #2563EB !important; color: #FFFFFF !important; border: none !important; border-radius: 6px !important; 
        }
        .stButton>button:hover { background-color: #1D4ED8 !important; }
        .stButton>button *, div[data-testid="stFileUploader"] button * { color: #FFFFFF !important; }
        
        /* Metrics & Chat Bubbles */
        div[data-testid="metric-container"] { 
            background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important; border-radius: 8px; padding: 12px; 
        }
        div[data-testid="metric-container"] * { color: #0F172A !important; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important; border-radius: 12px; }
        #MainMenu, footer { visibility: hidden !important; }
        </style>
        """
    else:
        style_payload = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600&display=swap');
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
            background-color: #0B0F19 !important; color: #E2E8F0 !important; font-family: 'Inter', sans-serif; 
        }
        [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] { 
            background-color: #111827 !important; border-right: 1px solid #1F2937 !important; 
        }
        p, h1, h2, h3, span, label, [data-testid="stWidgetLabel"] p, .stMarkdown div p { 
            color: #E2E8F0 !important; 
        }
        
        /* Chat Input Container */
        [data-testid="stBottomBlockContainer"], [data-testid="stBottom"], div[class*="stChatInput"] { 
            background-color: #0B0F19 !important; 
        }
        [data-testid="stChatInput"] textarea { 
            background-color: #1F2937 !important; 
            color: #E2E8F0 !important; 
            -webkit-text-fill-color: #E2E8F0 !important;
            caret-color: #E2E8F0 !important;
            border: 1px solid #4B5563 !important; 
        }
        [data-testid="stChatInput"] textarea::placeholder { 
            color: #9CA3AF !important; 
            -webkit-text-fill-color: #9CA3AF !important;
        }
        [data-testid="stChatInput"] button svg { fill: #E2E8F0 !important; color: #E2E8F0 !important; }
        
        /* File Uploader */
        [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploadDropzone"], section.stFileUploaderDropzone { 
            background-color: #1F2937 !important; border: 2px dashed #374151 !important; 
        }
        [data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploadDropzone"] * { 
            color: #E2E8F0 !important; fill: #E2E8F0 !important; 
        }
        
        /* Standard Buttons */
        .stButton>button, div[data-testid="stFileUploader"] button { 
            background-color: #3B82F6 !important; color: #FFFFFF !important; border: none !important; border-radius: 6px !important; 
        }
        .stButton>button:hover { background-color: #2563EB !important; }
        .stButton>button *, div[data-testid="stFileUploader"] button * { color: #FFFFFF !important; }
        
        /* Metrics & Chat Bubbles */
        div[data-testid="metric-container"] { 
            background-color: #1F2937 !important; border: 1px solid #374151 !important; border-radius: 8px; padding: 12px; 
        }
        div[data-testid="metric-container"] * { color: #E2E8F0 !important; }
        .stChatMessage { background-color: #1F2937 !important; border: 1px solid #374151 !important; border-radius: 12px; }
        #MainMenu, footer { visibility: hidden !important; }
        </style>
        """
    st.markdown(style_payload, unsafe_allow_html=True)

inject_theme_engine(st.session_state.theme)

# --- 5. INTERFACE CONTROL SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.radio("🎨 UI Theme", ["Dark", "Light"], key="theme", horizontal=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    col1.metric("Indexed Chunks", st.session_state.total_chunks)
    col2.metric("Total Queries", st.session_state.stats["queries"])
    st.divider()
    
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("Process PDFs", use_container_width=True) and uploaded_files:
        with st.spinner("Running Advanced RAG Pipeline..."):
            for f in uploaded_files:
                path = os.path.join(CONFIG.DOCS_DIR, f.name)
                with open(path, "wb") as out: 
                    out.write(f.getbuffer())
                rag_service.process_pdf(path, f.name, round(f.size / 1048576, 2))
            
            del st.session_state.total_chunks
            del st.session_state.stats
            st.success("Indexing verified!")
            time.sleep(0.5)
            st.rerun()
            
    st.divider()
    top_k = st.slider("Top K Results", min_value=1, max_value=10, value=3)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.20, step=0.05)
    
    st.divider()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# --- 6. INTERFACE MAIN CHAT CONSOLE ---
st.title("🤖 AI PDF Knowledge Assistant")
st.markdown("Ask questions about your uploaded enterprise documents.")

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if st.session_state.total_chunks == 0:
            st.warning("⚠️ Please upload and process a PDF document first.")
            st.stop()
            
        with st.spinner("Executing Semantic Search..."):
            start_time = time.time()
            
            results = rag_service.search_similar(prompt, top_k=top_k, threshold=0.0)
            context_text = "\n\n".join([doc.page_content for doc, score in results])
            
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", CONFIG.default_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])
            
            # THE FIX: Directly instantiate the LLM here instead of using the buggy .bind() wrapper
            dynamic_llm = ChatOllama(model=CONFIG.LLM_MODEL, temperature=temperature)
            
            chain = prompt_template | dynamic_llm | StrOutputParser()
            
            full_response = st.write_stream(chain.stream({
                "context": context_text,
                "input": prompt,
                "chat_history": st.session_state.chat_history
            }))
            
            gen_time = round(time.time() - start_time, 2)
            db_service.update_statistics(gen_time)
            del st.session_state.stats
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.extend([HumanMessage(content=prompt), AIMessage(content=full_response)])