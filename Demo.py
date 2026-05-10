import streamlit as st
from google import genai  # Note the change in import
from PyPDF2 import PdfReader

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋")

# Use the new Client structure from your screenshot
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Client setup failed: {e}")

# --- 2. LOGIC ---
if 'master_syllabus' not in st.session_state:
    st.session_state['master_syllabus'] = "Class 6 Hindi: Nouns, Adjectives, Pronouns."

with st.sidebar:
    st.image("https://cybergeontechnologies.com/wp-content/uploads/2024/02/cybergeon-logo.png")
    syllabus_input = st.text_area("Master Syllabus", value=st.session_state['master_syllabus'], height=200)
    st.session_state['master_syllabus'] = syllabus_input

# --- 3. MAIN APP ---
st.title("Neo-Edu: Agentic School Administration")
uploaded_file = st.file_uploader("Upload Teacher's Draft (PDF)", type="pdf")

if uploaded_file and st.button("Run Agentic Audit"):
    with st.spinner("Gemini 3 is thinking..."):
        # Extract PDF Text
        reader = PdfReader(uploaded_file)
        paper_text = " ".join([page.extract_text() for page in reader.pages])
        
        # New Gemini 3 Generate Content Syntax
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"Audit this paper against syllabus: {st.session_state['master_syllabus']}. Paper: {paper_text}. Draft Hindi notice."
        )
        
        st.subheader("📋 Audit Report")
        st.markdown(response.text)
        st.balloons()
