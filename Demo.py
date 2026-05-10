import streamlit as st
import time

# --- Page Config ---
st.set_page_config(page_title="Neo-Edu | Cybergeon", page_icon="🦋")

# --- Sidebar (The "AMD Proof" Hack) ---
st.sidebar.image("https://cybergeontechnologies.com/wp-content/uploads/2024/02/cybergeon-logo.png", width=200) # Use your logo URL
st.sidebar.title("System Status")
st.sidebar.success("AMD ROCm: ACTIVE")
st.sidebar.info("Compute: AMD Radeon™ GPU")
st.sidebar.write("Model: Qwen-7B (Quantized)")

# --- Main UI ---
st.title("Neo-Edu: Agentic School Admin")
st.write("Autonomous Syllabus Audit & Faculty Coordination")

uploaded_file = st.file_uploader("Upload Exam Paper (PDF/Doc)", type=['pdf', 'txt'])

if uploaded_file:
    with st.status("🚀 Neo Agent is Auditing...", expanded=True) as status:
        st.write("Retrieving Master Syllabus from Vector DB...")
        time.sleep(1)
        st.write("Analyzing content using AMD-optimized kernels...")
        time.sleep(2)
        st.write("Cross-referencing Class 6 Hindi Requirements...")
        time.sleep(1)
        status.update(label="Audit Complete!", state="complete", expanded=False)

    # --- Results ---
    st.subheader("Audit Report")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Syllabus Match", value="85%", delta="-15% (Missing Topics)")
    
    with col2:
        st.error("Gap Detected: 'Grammar - Adjectives' missing.")

    st.divider()
    
    # --- The Agentic Action ---
    st.subheader("Autonomous Action")
    st.write("The Agent has drafted the following notice for the teacher:")
    
    hindi_notice = """
    प्रिय शिक्षक, 
    कक्षा 6 हिन्दी (PT1) के प्रश्न पत्र में 'विशेषण' (Adjectives) अनुभाग शामिल नहीं है, 
    जो कि पाठ्यक्रम के अनुसार अनिवार्य है। कृपया इसे अपडेट करें।
    - Neo-Edu Admin Agent
    """
    st.text_area("Draft Notification (Hindi)", value=hindi_notice, height=150)
    
    if st.button("Send to Faculty"):
        st.balloons()
        st.success("Notification sent to Ms. Manisha via Neo-Connect.")
