import os
import streamlit as st
import time
from config import CONFIG

def apply_custom_css() -> None:
    """Premium Custom CSS removing all Streamlit branding."""
    css = """
    <style>
        /* Hide Streamlit Defaults */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Global Typography & Background */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        html, body, .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #0B0F19;
            color: #E2E8F0;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1F2937;
            padding-top: 2rem;
        }
        
        /* Dashboard Cards */
        div[data-testid="metric-container"] {
            background-color: #1F2937;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #374151;
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: #1F2937;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #374151;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Input Field */
        .stChatInputContainer {
            padding-bottom: 20px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #3B82F6;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #2563EB;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        /* Expander / Citations */
        .streamlit-expanderHeader {
            background-color: #111827 !important;
            border-radius: 8px;
            border: 1px solid #374151;
        }
        
        /* Highlight Simulation */
        mark {
            background-color: rgba(234, 179, 8, 0.2);
            color: #FCD34D;
            padding: 2px 4px;
            border-radius: 4px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def stream_text(text: str):
    """Simulates typing animation for the LLM."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)