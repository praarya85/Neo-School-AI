import streamlit as st
import time

# --- Configuration & Data ---
# This acts as your "Mini Vector DB" for now. Easily expandable.
SYLLABUS_DB = {
    "Class 6": {
        "Hindi": ["विशेषण", "संज्ञा", "पर्यायवाची", "मुहावरे"],
        "English": ["Adjectives", "Nouns", "Tenses", "Punctuations"]
    },
    "Class 7": {
        "Hindi": ["संधि", "अलंकार", "समास"],
        "English": ["Active Passive", "Direct Indirect", "Clauses"]
    }
}

# Faculty Mapping for Neo-Connect
FACULTY_DB = {
    "Class 6 Hindi": "Ms. Manisha",
    "Class 6 English": "Ms. Riya",
    "Class 7 Hindi": "Ms. Priyanka",
    "Class 7 English": "Ms. Leena"
}

# --- Page Config ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; }
    .stTextArea textarea { font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cybergeontechnologies.com/logo.jpg", width=200) # Ensure URL is valid
    st.title("Neo-Edu System")
    st.success("Status: Engine Active")
    st.info("Mode: Autonomous Audit")
    st.divider()
    st.write("**Cybergeon Technologies**")
    st.caption("v2.1.0-Dynamic-Beta")

# --- Main UI ---
st.title("🦋 Neo-Edu: Agentic School Admin")
st.write("Autonomous Syllabus Audit & Faculty Coordination")

# User Selections
col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    selected_class = st.selectbox("Target Class", list(SYLLABUS_DB.keys()))
with col_sel2:
    selected_subject = st.selectbox("Subject", list(SYLLABUS_DB[selected_class].keys()))

uploaded_file = st.file_uploader("Upload Exam Paper (TXT for this demo)", type=['txt'])

if uploaded_file:
    # Read content
    raw_text = uploaded_file.read().decode("utf-8")
    
    with st.status("🚀 Neo Agent is Auditing...", expanded=True) as status:
        st.write("Scanning document content...")
        time.sleep(1)
        
        # Dynamic Audit Logic
        required_topics = SYLLABUS_DB[selected_class][selected_subject]
        found_topics = [t for t in required_topics if t in raw_text]
        missing_topics = list(set(required_topics) - set(found_topics))
        
        match_score = int((len(found_topics) / len(required_topics)) * 100)
        
        st.write(f"Comparing against {selected_class} {selected_subject} Master Syllabus...")
        time.sleep(1)
        status.update(label="Audit Complete!", state="complete", expanded=False)

    # --- Results Display ---
    st.subheader("Audit Report")
    c1, c2 = st.columns(2)
    
    with c1:
        delta_val = f"{match_score - 100}%" if match_score < 100 else "Perfect"
        st.metric(label="Syllabus Match", value=f"{match_score}%", delta=delta_val)
    
    with c2:
        if missing_topics:
            st.error(f"Gap Detected: {', '.join(missing_topics)} missing.")
        else:
            st.success("Syllabus fully covered in this paper.")

    if missing_topics:
        st.divider()
        st.subheader("Autonomous Action")
        
        # Identify Target Teacher
        teacher_key = f"{selected_class} {selected_subject}"
        teacher_name = FACULTY_DB.get(teacher_key, "Subject Teacher")
        
        # Dynamic Hindi Notice
        hindi_notice = f"""प्रिय {teacher_name}, 

{selected_class} {selected_subject} (PT1) के प्रश्न पत्र में निम्नलिखित विषय शामिल नहीं हैं:
{', '.join(missing_topics)}।

यह पाठ्यक्रम (Syllabus) के अनुसार अनिवार्य हैं। कृपया प्रश्न पत्र अपडेट करें।

- Neo-Edu Admin Agent"""

        st.text_area("Draft Notification (Hindi)", value=hindi_notice, height=200)
        
        if st.button(f"Send to {teacher_name}"):
            st.balloons()
            st.success(f"Notification successfully pushed to {teacher_name} via Neo-Connect.")
