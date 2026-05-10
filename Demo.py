import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. CONFIGURATION & BRANDING ---
# Use your actual logo URL here
LOGO_URL = "https://via.placeholder.com/150" 

st.set_page_config(
    page_title="Neo-Edu | Cybergeon Technologies",
    page_icon="🦋",
    layout="wide"
)

# --- 2. THE ULTRA-RICH "SOBER" CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Professional Background */
    .main {{
        background-color: #fcfcfd;
    }}

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0;
    }}

    /* Cybergeon Primary Button */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.7rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
        transform: translateY(-2px);
    }}

    /* Result Card Styling */
    .audit-card {{
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        line-height: 1.6;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. CORE LOGIC & REASONING ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Streamlit Secrets.")
    st.stop()

# Using stable model ID for reliable performance
MODEL_ID = 'gemini-1.5-flash' 
model = genai.GenerativeModel(MODEL_ID)

def extract_text(file):
    try:
        reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except Exception as e:
        st.error(f"Read Error: {e}")
        return ""

def run_ai_audit(exam_text, syllabus_text):
    prompt = f"""
    You are Neo-Edu, an expert AI School Administrator for Cybergeon Technologies.
    Compare the [EXAM PAPER] against the [MASTER SYLLABUS].
    
    Provide:
    1. A percentage match.
    2. List of topics missing in the exam.
    3. Any questions that are OUTSIDE the provided syllabus.
    4. Professional feedback for faculty in both English and Hindi.

    EXAM: {exam_text[:15000]}
    SYLLABUS: {syllabus_text[:15000]}
    """
    response = model.generate_content(prompt)
    return response.text

# --- 4. UI STRUCTURE ---
with st.sidebar:
    st.image(LOGO_URL, width=80)
    st.markdown("### Cybergeon\n**Technologies**")
    st.divider()
    st.markdown("#### Engine Settings")
    st.caption("Mode: High-Reasoning")
    st.caption("Agent: Neo-Edu 2.5")

# Header
st.markdown("# 🦋 Neo-Edu: <span style='color:#4f46e5'>Syllabus Auditor</span>", unsafe_allow_html=True)
st.markdown("Focusing on educational compliance and faculty excellence.")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📄 Exam Paper")
    exam_file = st.file_uploader("Upload Question Paper (PDF)", type=['pdf'])

with col2:
    st.markdown("### 📚 Master Syllabus")
    syll_file = st.file_uploader("Upload Syllabus Reference (PDF)", type=['pdf'])

# --- 5. THE AUDIT PROCESS ---
if exam_file and syll_file:
    if st.button("🚀 INITIATE DEEP AUDIT"):
        with st.status("Neo is analyzing documents...", expanded=True) as status:
            e_text = extract_text(exam_file)
            s_text = extract_text(syll_file)
            
            if e_text and s_text:
                analysis = run_ai_audit(e_text, s_text)
                status.update(label="Audit Complete", state="complete")
                
                st.markdown("### 📊 Analysis Result")
                st.markdown(f'<div class="audit-card">{analysis}</div>', unsafe_allow_html=True)
                
                st.write("##")
                if st.button("📧 Send to Faculty Portal"):
                    st.balloons()
                    st.success("Analysis dispatched to Cybergeon Management.")
            else:
                status.update(label="Parsing Error", state="error")
                st.error("Could not extract enough text from the PDFs. Please check the file quality.")
else:
    st.write("##")
    st.info("Waiting for document upload to begin the analysis.")
