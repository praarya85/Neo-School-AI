import streamlit as st
import google.generativeai as genai
import pdfplumber  # Better for Hindi/Devanagari extraction

# --- 1. CONFIGURATION & BRANDING ---
LOGO_URL = "https://cybergeontechnologies.com/logo.jpg" 

st.set_page_config(
    page_title="Neo-Edu | Cybergeon Technologies",
    page_icon="🦋",
    layout="wide"
)

# --- 2. THE ULTRA-RICH "SOBER" CSS (Updated for Hindi Support) ---
st.markdown(f"""
<style>
    /* Adding Noto Sans Devanagari for clean Hindi rendering */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Noto+Sans+Devanagari:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;
    }}

    .main {{
        background-color: #fcfcfd;
    }}

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
        line-height: 1.8;
        color: #1f2937;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. CORE LOGIC & REASONING ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Streamlit Secrets.")
    st.stop()

MODEL_ID = 'gemini-2.5-flash' 
model = genai.GenerativeModel(MODEL_ID)

def extract_text(file):
    try:
        # Using pdfplumber for superior Hindi text extraction
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
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
    
    Ensure Hindi text is generated in clear, standard Devanagari script.

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
    st.caption("Agent: Neo-Edu 2.5 (Hindi Optimized)")

# Header
st.markdown("# 🦋 Neo-Edu: <span style='color:#4f46e5'>Syllabus Auditor</span>", unsafe_allow_html=True)
st.markdown("Focusing on educational compliance and faculty excellence for the K-12 market.")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📄 Exam Paper")
    exam_file = st.file_uploader("Upload Question Paper (PDF)", type=['pdf'])

with col2:
    st.markdown("### 📚 Master Syllabus")
    syll_file = st.file_uploader("Upload Syllabus Reference (PDF)", type=['pdf'])

# --- 5. THE AUDIT PROCESS & DOWNLOAD LOGIC ---
if exam_file and syll_file:
    if st.button("🚀 INITIATE DEEP AUDIT"):
        with st.status("Neo is analyzing documents...", expanded=True) as status:
            e_text = extract_text(exam_file)
            s_text = extract_text(syll_file)
            
            if e_text and s_text:
                analysis = run_ai_audit(e_text, s_text)
                st.session_state['last_analysis'] = analysis
                status.update(label="Audit Complete", state="complete")
            else:
                status.update(label="Parsing Error", state="error")
                st.error("Could not extract enough text. Ensure the PDFs are not scanned images.")

if 'last_analysis' in st.session_state:
    st.markdown("### 📊 Analysis Result")
    st.markdown(f'<div class="audit-card">{st.session_state["last_analysis"]}</div>', unsafe_allow_html=True)
    
    st.write("##")
    
    col_dl, col_portal = st.columns([1.5, 4])
    
    with col_dl:
        # Professional header for the download file
        report_header = f"NEO-EDU AUDIT REPORT\nGenerated by Cybergeon Technologies\nExam: {exam_file.name}\n" + ("-"*40) + "\n\n"
        full_report = report_header + st.session_state['last_analysis']
        
        # Encoding as UTF-8 to preserve Hindi characters in the download
        st.download_button(
            label="📥 Download Audit Report",
            data=full_report.encode('utf-8'),
            file_name=f"NeoEdu_Audit_{exam_file.name.replace('.pdf', '')}.txt",
            mime="text/plain"
        )
    
    with col_portal:
        if st.button("📧 Send to Faculty Portal"):
            st.balloons()
            st.success("Analysis dispatched to Cybergeon Management.")
else:
    st.write("##")
    st.info("Waiting for document upload to begin the analysis.")
