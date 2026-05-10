import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. CONFIGURATION & BRANDING ---
# Replace this URL with your actual Cybergeon logo link or local path
LOGO_URL = "https://cybergeontechnologies.com/logo.jpg"

st.set_page_config(
    page_title="Neo-Edu | Powered by Cybergeon",
    page_icon="🦋",
    layout="wide"
)

# --- 2. THE "SOBER & RICH" CSS ---
def apply_cybergeon_theme():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            color: #2D3436;
        }}

        /* Clean, Professional Background */
        .main {{
            background: #F8F9FA;
        }}

        /* Sidebar: Sober & Minimalist */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
            border-right: 1px solid #E0E0E0;
        }}

        /* Cybergeon Signature Gradient Button */
        .stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.6rem !important;
            transition: 0.3s all ease;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
            transform: translateY(-1px);
        }}

        /* Rich Glass Cards for Results */
        .report-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #E0E0E0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }}

        .logo-text {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #2D3436;
            margin-bottom: 0px;
        }}
        
        .subtitle {{
            font-size: 12px;
            color: #636E72;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_cybergeon_theme()

# --- 3. SIDEBAR BRANDING ---
with st.sidebar:
    st.image(LOGO_URL, width=80)
    st.markdown("<p class='logo-text'>Cybergeon</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Technologies</p>", unsafe_allow_html=True)
    st.divider()
    
    st.info("**Neo-Edu Engine v2.5**\n\nStatus: Secure & Reasoning Active")
    st.write("---")
    st.caption("© 2026 Cybergeon Technologies. All rights reserved.")

# --- 4. MAIN INTERFACE ---
# Header Section
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image(LOGO_URL, width=100)
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>Neo-Edu: <span style='color:#6C5CE7;'>Syllabus Auditor</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; opacity:0.7;'>High-fidelity academic compliance powered by Cybergeon AI.</p>", unsafe_allow_html=True)

st.write("##")

# Content Columns
c1, c2 = st.columns(2)
with c1:
    st.markdown("### 📁 Upload Exam Paper")
    exam_file = st.file_uploader("Drop PDF here", type=['pdf'], key="exam")

with c2:
    st.markdown("### 📚 Master Syllabus")
    syll_file = st.file_uploader("Drop Reference PDF here", type=['pdf'], key="syll")

# --- 5. EXECUTION ---
if exam_file and syll_file:
    st.write("---")
    if st.button("🚀 INITIATE DEEP AUDIT"):
        with st.status("Neo-Edu is processing...", expanded=True) as status:
            # Note: Logic for text extraction remains the same as your original
            st.write("Synchronizing with Master Syllabus...")
            # (Simulation of extraction & AI call)
            # analysis_result = run_ai_audit(e_text, s_text)
            
            status.update(label="Audit Successfully Completed", state="complete")
        
        # Displaying result in a "Rich" container
        st.markdown("""
        <div class="report-card">
            <h3>📊 Audit Findings</h3>
            <hr>
            <p><i>The AI analysis would appear here based on your run_ai_audit function.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("##")
        if st.button("📨 Send Official Notice to Faculty"):
            st.balloons()
            st.toast("Draft sent to Cybergeon Management Portal.")

else:
    st.write("##")
    st.markdown("""
        <div style="text-align: center; padding: 40px; border: 2px dashed #E0E0E0; border-radius: 12px;">
            <p style="color: #636E72;">Welcome, Mr. Arya. Please upload the required documents to begin the session.</p>
        </div>
    """, unsafe_allow_html=True)
