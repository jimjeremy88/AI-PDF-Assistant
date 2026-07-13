import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from core.use_cases import RAGUseCase
from config import CONFIG
from utils.helpers import apply_custom_css, stream_text
from utils.exporter import export_to_markdown, export_to_pdf

class StreamlitUI:
    def __init__(self, use_case: RAGUseCase) -> None:
        self.use_case = use_case

    def _init_state(self) -> None:
        if "messages" not in st.session_state: st.session_state.messages = []
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        if "uploaded_count" not in st.session_state: st.session_state.uploaded_count = 0
        if "avg_time" not in st.session_state: st.session_state.avg_time = 0.0
        if "total_queries" not in st.session_state: st.session_state.total_queries = 0

    def render(self) -> None:
        st.set_page_config(page_title="Enterprise AI", page_icon="⚡", layout="wide")
        apply_custom_css()
        self._init_state()
        self._render_sidebar()
        self._render_chat()

    def _render_sidebar(self) -> None:
        with st.sidebar:
            st.title("⚡ Settings & Dashboard")
            
            # Document Upload
            st.subheader("Knowledge Base")
            uploaded_files = st.file_uploader("Upload Documents", type="pdf", accept_multiple_files=True)
            if st.button("Index Documents", use_container_width=True) and uploaded_files:
                with st.spinner("Indexing into Vector Database..."):
                    file_paths = []
                    for f in uploaded_files:
                        path = os.path.join(CONFIG.docs_dir, f.name)
                        with open(path, "wb") as out: out.write(f.getbuffer())
                        file_paths.append(path)
                    
                    try:
                        chunks = self.use_case.process_new_documents(file_paths)
                        st.session_state.uploaded_count = len(uploaded_files)
                        st.success(f"Indexed {chunks} chunks.")
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.divider()
            
            # Dashboard Metrics
            stats = self.use_case.get_dashboard_stats()
            col1, col2 = st.columns(2)
            col1.metric("Indexed Chunks", stats["chunks_indexed"])
            col2.metric("Documents", st.session_state.uploaded_count)
            
            col3, col4 = st.columns(2)
            col3.metric("LLM", CONFIG.llm_model)
            col4.metric("Avg Response", f"{st.session_state.avg_time}s")

            st.divider()
            
            # Advanced Settings
            with st.expander("Model Configuration"):
                st.session_state.top_k = st.slider("Top K", 1, 10, CONFIG.chunk_overlap if CONFIG.chunk_overlap < 10 else 3)
                st.session_state.temp = st.slider("Temperature", 0.0, 1.0, 0.2)
                st.session_state.sys_prompt = st.text_area("System Prompt", CONFIG.default_system_prompt, height=150)

    def _render_chat(self) -> None:
        st.title("Enterprise AI Knowledge Assistant")
        st.markdown("Secure, Local, and Architecture-Driven RAG Application.")

        # Render History
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("timestamp"):
                    st.caption(f"🕒 {msg['timestamp']} | ⏱️ {msg.get('time', 0)}s")
                
                # Render Citations gracefully
                if msg.get("sources"):
                    with st.expander("📚 View Source Citations"):
                        for idx, source in enumerate(msg["sources"]):
                            filename = os.path.basename(source.metadata.get('source', 'Unknown File'))
                            page = source.metadata.get('page', 0)
                            st.markdown(f"**📄 File:** `{filename}` | **📑 Page:** `{page}` | **🎯 Similarity:** `{source.score}%`")
                            # Highlight Simulation
                            st.markdown(f"> <mark>{source.content}</mark>", unsafe_allow_html=True)
                            st.divider()
                
        # Action Bar (Export / Controls)
        if st.session_state.messages:
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_history = []
                st.rerun()
            if c2.button("🔄 Regenerate", use_container_width=True) and len(st.session_state.messages) >= 2:
                # Remove last AI message and re-run last prompt
                last_prompt = st.session_state.messages[-2]["content"]
                st.session_state.messages = st.session_state.messages[:-2]
                st.session_state.chat_history = st.session_state.chat_history[:-2]
                self._handle_prompt(last_prompt)
            
            # Exports
            md_str = export_to_markdown(st.session_state.messages)
            c3.download_button("📥 Markdown", md_str, "chat.md", use_container_width=True)
            
            pdf_path = export_to_pdf(st.session_state.messages)
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    c4.download_button("📥 PDF", pdf_file, "chat.pdf", use_container_width=True)

        # Chat Input
        if prompt := st.chat_input("Ask a question based on your documents..."):
            self._handle_prompt(prompt)

    def _handle_prompt(self, prompt: str):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Analyzing context..."):
                    response = self.use_case.generate_response(
                        question=prompt,
                        chat_history=st.session_state.chat_history,
                        temperature=st.session_state.temp,
                        top_k=st.session_state.top_k,
                        system_prompt=st.session_state.sys_prompt
                    )
                
                # Streaming Output
                st.write_stream(stream_text(response.answer))
                
                # Metrics Calculation
                st.session_state.total_queries += 1
                curr_total = (st.session_state.avg_time * (st.session_state.total_queries - 1)) + response.generation_time
                st.session_state.avg_time = round(curr_total / st.session_state.total_queries, 2)

                # State Updates
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.answer,
                    "sources": response.sources,
                    "timestamp": response.timestamp,
                    "time": response.generation_time
                })
                
                st.session_state.chat_history.extend([
                    HumanMessage(content=prompt),
                    AIMessage(content=response.answer)
                ])
                st.rerun()

            except Exception as e:
                st.error("⚠️ Graceful Error: The system encountered an issue processing your request.")
                with st.expander("Technical Details"):
                    st.code(str(e))