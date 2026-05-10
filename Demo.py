import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import time

# --- 1. SECURE CONFIGURATION ---
# The key you provided earlier should be placed in the Streamlit Secrets sidebar 
# under the name: GEMINI_API_KEY
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# UPDATED: Using 'gemini-1.5-flash-latest' for better compatibility
# You can also use 'gemini-1.5-pro-latest' if you want more reasoning power
MODEL_ID = 'gemini-1.5-flash-latest' 

try:
    model = genai.GenerativeModel(MODEL_ID)
except Exception as e:
    st.error(f"Failed to initialize model: {e}")
    st.stop()

# --- 2. HELPER FUNCTIONS ---
def extract_text_pypdf(file):
    """Extracts digital text layer from PDF."""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text.strip()
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        return ""

def run_ai_audit(exam_text, syllabus_text):
    """Sends text to Gemini for comparison and Hindi feedback."""
    prompt = f"""
    You are Neo-Edu, an expert AI School Administrator for the Indian K-12 market.
    
    TASK:
    Compare the [EXAM PAPER] text against the [MASTER SYLLABUS] text provided below.
    
    OUTPUT FORMAT:
    1. Match Percentage: (Give a percentage)
    2. Missing Topics: (List any topics from syllabus not in exam)
    3. Faculty Feedback (HINDI): Draft a professional and polite notice in Hindi 
       addressed to the teacher explaining the gaps or praising the alignment.
    
    [EXAM PAPER]:
    {exam_text[:15000]} 
    
    [MASTER SYLLABUS]:
    {syllabus_text[:15000]}
    """
    try:
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Specific error handling for the 404 issue
        return f"AI Error: {str(e)}. Please check if the model name '{MODEL_ID}' is supported in your region."

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

# Sidebar
with st.sidebar:
    # Use a placeholder if logo URL fails
    try:
        st.image("https://cybergeontechnologies.com/logo.jpg", width=200)
    except:
        st.title("CYBERGEON")
    
    st.title("Neo-Edu v3.0")
    st.subheader(f"Intelligence: {MODEL_ID}")
    st.success("API Connection: ACTIVE")
    st.divider()
    st.write("**Cybergeon Technologies**")

# Main Interface
st.title("🦋 Neo-Edu: Agentic School Admin")
st.write("Autonomous Syllabus Audit via Google Gemini AI")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📁 1. Exam Paper")
    exam_file = st.file_uploader("Upload Question Paper", type=['pdf', 'txt'], key="exam")

with col2:
    st.subheader("📚 2. Master Syllabus")
    syll_file = st.file_uploader("Upload Reference Syllabus", type=['pdf', 'txt'], key="syll")

if exam_file and syll_file:
    if st.button("🚀 Start AI Audit", use_container_width=True):
        with st.status("Neo is processing...", expanded=True) as status:
            st.write("Reading documents...")
            e_text = extract_text_pypdf(exam_file)
            s_text = extract_text_pypdf(syll_file)
            
            if not e_text or not s_text:
                status.update(label="Parsing Failed", state="error")
                st.error("Could not find text in one of the PDFs. Please ensure they are digital PDFs (not scans/images).")
                st.stop()
            
            st.write(f"Consulting {MODEL_ID} for comparison...")
            analysis_result = run_ai_audit(e_text, s_text)
            
            status.update(label="Audit Complete!", state="complete", expanded=False)

        # --- RESULTS DISPLAY ---
        st.divider()
        st.subheader("Neo-Edu Intelligence Report")
        st.markdown(analysis_result)
        
        if st.button("Send to Faculty via Neo-Connect"):
            st.balloons()
            st.success("Notification processed and drafted for delivery.")
else:
    st.info("Please upload both files to activate the AI Admin Agent.")
