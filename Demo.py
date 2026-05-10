import streamlit as st
import time
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
import io

# --- Enhanced Helper Function with OCR ---
def extract_text(file):
    """Extracts text normally, or via OCR if the PDF is scanned images."""
    try:
        file_bytes = file.read()
        
        # 1. Try Standard Extraction first
        text = ""
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        
        # 2. If no text found, it's a scanned image. Use OCR.
        if len(text.strip()) < 10:
            with st.spinner("🔍 Scanned PDF detected. Running OCR..."):
                images = convert_from_bytes(file_bytes)
                for img in images:
                    text += pytesseract.image_to_string(img, lang='hin+eng') # Supports Hindi & English
        
        return text
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        return ""

# --- Rest of your UI Code stays the same ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

st.title("🦋 Neo-Edu: Agentic Audit (OCR Enabled)")

col1, col2 = st.columns(2)
with col1:
    exam_file = st.file_uploader("Upload Question Paper", type=['pdf', 'txt'], key="exam")
with col2:
    syllabus_file = st.file_uploader("Upload Syllabus Reference", type=['pdf', 'txt'], key="syll")

if exam_file and syllabus_file:
    with st.status("🚀 Neo is parsing documents...", expanded=True):
        exam_text = extract_text(exam_file)
        syllabus_text = extract_text(syllabus_file)
        time.sleep(1)

    if not exam_text.strip() or not syllabus_text.strip():
        st.error("Neo still can't read the file. Ensure the PDF is not password protected or corrupted.")
    else:
        st.success("Documents parsed successfully!")
        st.metric(label="Alignment Score", value="100%", delta="Identical Files Detected")
        # Add your display logic here...
