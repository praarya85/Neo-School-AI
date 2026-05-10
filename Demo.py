import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

# FIX: Use 'gemini-1.5-flash' or 'gemini-pro'. 
# Ensure your API Key is in Streamlit Secrets!
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using 'gemini-1.5-flash' - if this fails, change to 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- 2. THE "STICKY" SYLLABUS LOGIC ---
# This sets a permanent default so you don't have to re-type it.
if 'master_syllabus' not in st.session_state:
    st.session_state['master_syllabus'] = """Class 6 Hindi PT1:
1. Nouns (संज्ञा)
2. Pronouns (सर्वनाम)
3. Adjectives (विशेषण)
4. Letter Writing."""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cybergeontechnologies.com/wp-content/uploads/2024/02/cybergeon-logo.png")
    st.header("Master Settings")
    
    # User can edit it, but it stays pre-filled
    syllabus_input = st.text_area("Master Syllabus", 
                                  value=st.session_state['master_syllabus'], 
                                  height=250)
    st.session_state['master_syllabus'] = syllabus_input

# --- 4. MAIN APP ---
st.title("Neo-Edu: Agentic School Administration")
uploaded_file = st.file_uploader("Step 2: Upload Teacher's Draft (PDF)", type="pdf")

if uploaded_file:
    if st.button("Step 3: Run Agentic Audit"):
        with st.spinner("Neo Agent is auditing against Master Syllabus..."):
            try:
                # Extract text from PDF
                reader = PdfReader(uploaded_file)
                paper_text = " ".join([page.extract_text() for page in reader.pages])
                
                # Agentic Loop
                prompt = f"""
                Audit this exam paper against the master syllabus.
                SYLLABUS: {st.session_state['master_syllabus']}
                EXAM PAPER: {paper_text}
                
                Provide:
                1. Missing Topics List
                2. A correction notice for the teacher in HINDI.
                """
                
                response = model.generate_content(prompt)
                
                st.subheader("📋 Audit Report")
                st.markdown(response.text)
                st.balloons()
                
            except Exception as e:
                st.error(f"Audit Failed: {e}")
                st.info("Check if your Gemini API Key supports the 'gemini-1.5-flash' model.")
