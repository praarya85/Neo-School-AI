import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- Configure Gemini ---
# Get your key from: https://aistudio.google.com/
genai.configure(api_key="YOUR_FREE_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def analyze_with_neo(exam_text, syllabus_text):
    prompt = f"""
    You are Neo-Edu, an AI School Admin. 
    Compare the following EXAM PAPER text with the MASTER SYLLABUS text.
    
    1. Identify missing topics.
    2. Give a match percentage (0-100%).
    3. Draft a polite notification in Hindi for the teacher if gaps exist.
    
    EXAM PAPER: {exam_text[:5000]}
    MASTER SYLLABUS: {syllabus_text[:5000]}
    """
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
st.title("🦋 Neo-Edu: AI Powered Audit")

exam_file = st.file_uploader("Upload Exam Paper", type=['pdf'])
syll_file = st.file_uploader("Upload Syllabus", type=['pdf'])

if exam_file and syll_file:
    if st.button("Run AI Audit"):
        with st.spinner("Neo is thinking..."):
            e_text = get_pdf_text(exam_file)
            s_text = get_pdf_text(syll_file)
            
            # The Magic happens here
            analysis = analyze_with_neo(e_text, s_text)
            
            st.subheader("Neo's Intelligence Report")
            st.write(analysis)
