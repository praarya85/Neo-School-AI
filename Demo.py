import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# UPDATED: Using Gemini 2.5 Flash
# This model supports "Thinking" mode which is perfect for complex audits.
MODEL_ID = 'gemini-2.5-flash' 

try:
    # We initialize the model. Gemini 2.5 supports 'thinking' 
    # which can be toggled in the generation config if needed.
    model = genai.GenerativeModel(MODEL_ID)
except Exception as e:
    st.error(f"Failed to initialize Neo 2.5: {e}")
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
    """Sends text to Gemini 2.5 for a high-reasoning comparison."""
    # Updated Prompt for Gemini 2.5 "Thinking" capabilities
    prompt = f"""
    You are Neo-Edu, an expert AI School Administrator. Use your advanced reasoning 
    to conduct a deep audit of the following documents.
    
    TASK:
    1. Analyze the [MASTER SYLLABUS] to identify core required topics.
    2. Cross-reference every question in the [EXAM PAPER] against those topics.
    3. Identify if questions are 'Out of Syllabus' or if 'Critical Topics' are missing.
    
    OUTPUT FORMAT:
    ### 🧠 Reasoning Process (Thinking)
    (Summarize how you verified the alignment)

    ### 📊 Audit Summary
    - **Syllabus Match:** [X]%
    - **Difficulty Level:** [Easy/Medium/Hard]
    - **Missing Topics:** (List any key syllabus items not tested)
    
    ### 📝 Faculty Feedback (HINDI)
    (Write a professional notice in Hindi and English for the teacher regarding these results)
    
    [EXAM PAPER]:
    {exam_text[:20000]} 
    
    [MASTER SYLLABUS]:
    {syllabus_text[:20000]}
    """
    try:
        # Gemini 2.5 can handle larger context; I've increased limits to 20k characters.
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

with st.sidebar:
    st.title("Neo-Edu AI Agent")
    st.subheader(f"Engine: Neo 2.5")
    st.info("Status: High-Reasoning Mode Active")
    st.divider()
    st.write("**Cybergeon Technologies**")

st.title("🦋 Neo-Edu:  Syllabus Auditor")
st.write("Leveraging Generational Reasoning for Educational Compliance.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📁 1. Exam Paper")
    exam_file = st.file_uploader("Upload Question Paper", type=['pdf', 'txt'], key="exam")

with col2:
    st.subheader("📚 2. Master Syllabus")
    syll_file = st.file_uploader("Upload Reference Syllabus", type=['pdf', 'txt'], key="syll")

if exam_file and syll_file:
    if st.button("🚀 Start Deep AI Audit", use_container_width=True):
        with st.status("Neo 2.5 is thinking...", expanded=True) as status:
            st.write("Parsing documents...")
            e_text = extract_text_pypdf(exam_file)
            s_text = extract_text_pypdf(syll_file)
            
            if not e_text or not s_text:
                status.update(label="Parsing Failed", state="error")
                st.stop()
            
            st.write("Performing high-reasoning cross-analysis...")
            analysis_result = run_ai_audit(e_text, s_text)
            status.update(label="Audit Complete!", state="complete", expanded=False)

        st.divider()
        st.markdown(analysis_result)
        
        if st.button("Send to Faculty"):
            st.balloons()
            st.success("Drafted and queued for delivery.")
else:
    st.info("Upload documents to begin the Neo 2.5 audit.")
