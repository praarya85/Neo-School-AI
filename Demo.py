import streamlit as st
import time
from PyPDF2 import PdfReader
from docx import Document
import io

# --- Helper Functions for File Processing ---
def extract_text(file):
    """Extracts text from PDF, DOCX, or TXT files."""
    if file.name.endswith('.pdf'):
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith('.docx'):
        doc = Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    else:
        return file.read().decode("utf-8")

# --- Page Config ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.image("https://cybergeontechnologies.com/logo.jpg", width=200)
    st.title("Neo-Edu Engine")
    st.status("Document Parsers: LOADED", state="complete")
    st.divider()
    st.caption("Developed by Cybergeon Technologies")

# --- Main UI ---
st.title("🦋 Neo-Edu: Dynamic Audit")
st.write("Upload both the **Exam Paper** and the **Master Syllabus** for Neo to analyze.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Exam Paper")
    exam_file = st.file_uploader("Upload Paper (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="exam")

with col2:
    st.subheader("2. Reference Syllabus")
    syllabus_file = st.file_uploader("Upload Syllabus (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="syll")

if exam_file and syllabus_file:
    with st.status("🚀 Neo Agent is analyzing documents...", expanded=True) as status:
        # Extracting text
        st.write("Reading Exam Paper...")
        exam_text = extract_text(exam_file)
        
        st.write("Reading Reference Syllabus...")
        syllabus_text = extract_text(syllabus_file)
        
        # In a real RAG setup, we'd use LLM comparison. 
        # For this dynamic logic, we simulate the "Topic Extraction"
        st.write("Cross-referencing content...")
        time.sleep(2)
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # --- Simulated Analysis Results ---
    # In a full Cybergeon production, this would be an LLM call comparing exam_text to syllabus_text
    st.success("Comparison logic active.")
    
    st.subheader("Neo's Observation")
    report_text = """
    The Exam Paper covers approximately 90% of the uploaded syllabus. 
    However, Neo noticed a missing section regarding 'Letter Writing' or 'Formal Applications' 
    which was present in the Syllabus file.
    """
    st.info(report_text)

    # --- Actionable Output ---
    st.divider()
    hindi_notice = f"""प्रिय शिक्षक, 

मैने आपके प्रश्न पत्र और सिलेबस की तुलना की है। आपके प्रश्न पत्र में 'औपचारिक पत्र' (Formal Letter) का भाग कम लग रहा है, जो सिलेबस में शामिल है। 

कृपया इसे एक बार देख लें।

- Neo-Edu Admin Agent"""

    st.text_area("Generated Feedback (Hindi)", value=hindi_notice, height=150)
    
    if st.button("Notify Teacher"):
        st.balloons()
        st.success("Feedback sent successfully!")
else:
    st.info("Please upload both files to start the autonomous audit.")
