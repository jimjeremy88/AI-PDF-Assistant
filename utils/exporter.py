\import os
from typing import List, Dict
from fpdf import FPDF
from config import CONFIG

def export_to_markdown(messages: List[Dict]) -> str:
    md_content = "# Chat History Export\n\n"
    for msg in messages:
        role = "👤 User" if msg["role"] == "user" else "🤖 AI Assistant"
        md_content += f"### {role}\n{msg['content']}\n\n"
    return md_content

def export_to_pdf(messages: List[Dict]) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Assistant - Chat History", ln=True, align='C')
    pdf.ln(10)
    
    for msg in messages:
        role = "User" if msg["role"] == "user" else "AI Assistant"
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"{role}:", ln=True)
        
        pdf.set_font("Arial", size=11)
        # Handle encoding for PDF
        text = msg['content'].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=text)
        pdf.ln(5)
        
    filepath = os.path.join(CONFIG.settings_dir, "export.pdf")
    pdf.output(filepath)
    return filepath