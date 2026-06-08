# app.py
# This is the FACE of our application — what users actually see.
# Streamlit turns Python code into a web app instantly.
# No HTML, no CSS, no JavaScript needed!

import streamlit as st
from agent import run_agent

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🏥",
    layout="centered"
)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🏥 MediGuide AI")
st.subheader("Your AI-powered health information assistant")

st.warning("""
⚠️ **Important Disclaimer**
MediGuide provides general health information only.
It is NOT a substitute for professional medical advice.
Always consult a qualified healthcare professional.
""")

st.divider()

# ─────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────
st.markdown("### 📝 Describe Your Symptoms")
st.markdown("Be as specific as possible — mention duration, severity, and any other relevant details.")

symptoms = st.text_area(
    label="Your symptoms",
    placeholder="Example: I have had a headache and mild fever for 2 days. The headache is mostly on one side and gets worse with light.",
    height=120,
    label_visibility="collapsed"
)

# ─────────────────────────────────────────
# EXAMPLE BUTTONS
# ─────────────────────────────────────────
st.markdown("**Or try an example:**")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🤒 Fever & Headache"):
        symptoms = "I have had a fever of 38.5°C and a bad headache for 2 days"

with col2:
    if st.button("🤧 Cold & Sore Throat"):
        symptoms = "I have a sore throat, runny nose and feel tired for 3 days"

with col3:
    if st.button("🤕 Back Pain"):
        symptoms = "I have lower back pain that started 4 days ago, worse when sitting"

st.divider()

# ─────────────────────────────────────────
# RUN THE AGENT
# ─────────────────────────────────────────
if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
    
    if not symptoms:
        st.error("Please describe your symptoms first!")
    
    else:
        # Show a loading spinner while agent is working
        with st.spinner("🔍 Researching your symptoms from trusted medical sources..."):
            try:
                response = run_agent(symptoms)
                
                st.divider()
                st.markdown("### 📋 MediGuide Analysis")
                st.markdown(response)
                
                st.divider()
                st.info("""
                📚 **About MediGuide**
                This analysis was generated using real-time web research 
                from trusted medical sources (WHO, NHS, Mayo Clinic).
                Built with LangGraph + Groq + Tavily.
                """)
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.markdown("Please try again or rephrase your symptoms.")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Built by Khushi Gajjar | LangGraph + Groq + Tavily | 
<a href='https://github.com/khushimgajjar/mediguide-agent'>GitHub</a> | 
<a href='https://medium.com/@khushimgajjar'>Medium</a>
</div>
""", unsafe_allow_html=True)