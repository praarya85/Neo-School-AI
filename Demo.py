import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- PAGE CONFIG ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

# --- API INITIALIZATION ---
# Securely fetching the API Key from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key not found. Please configure GEMINI_API_KEY in Streamlit Secrets.")

# --- UTILITY FUNCTIONS ---
def get_pdf_text(file):
    reader = PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages])

def agent_audit(paper_text, syllabus):
    prompt = f"""
    Context: You are Neo-Edu, an AI Administrative Agent for Cybergeon Technologies.
    Task: Audit a teacher's exam paper against the provided syllabus.
    
    SYLLABUS: {syllabus}
    EXAM PAPER: {paper_text}
    
    1. List missing topics.
    2. Assess if the difficulty level matches the grade.
    3. IMPORTANT: Draft a correction notice for the teacher in HINDI.
    """
    response = model.generate_content(prompt)
    return response.text

# --- UI DESIGN ---
st.title("Neo-Edu: Agentic School Administration")
st.markdown("### Powered by **Cybergeon Technologies**")

with st.sidebar:
    st.image("https://cybergeontechnologies.com/wp-content/uploads/2024/02/cybergeon-logo.png")
    st.divider()
    syllabus_text = st.text_area("Step 1: Paste Master Syllabus", height=200, 
                                placeholder="e.g., Class 6 Hindi PT1 covers: Nouns, Adjectives, Letter Writing.")

# --- MAIN APP FLOW ---
uploaded_file = st.file_uploader("Step 2: Upload Teacher's Draft (PDF)", type="pdf")

if uploaded_file and syllabus_text:
    if st.button("Step 3: Run Agentic Audit"):
        with st.spinner("Agent is reasoning and cross-referencing..."):
            # 1. Extraction
            extracted_text = get_pdf_text(uploaded_file)
            
            # 2. Reasoning Loop
            audit_report = agent_audit(extracted_text, syllabus_text)
            
            # 3. Output
            st.divider()
            st.subheader("📋 Neo-Edu Audit Report")
            st.markdown(audit_report)
            
            if st.button("Confirm & Send to Faculty"):
                st.success("Notification sent via Neo-Connect Gateway.")
                st.balloons()
else:
    st.info("Please provide the syllabus in the sidebar and upload a PDF to begin.")
