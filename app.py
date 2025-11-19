import streamlit as st
import google.generativeai as genai

st.title("🛠️ System Diagnostic")

# 1. Configure API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 2. Ask Google what models are available
st.write("Contacting Google API to find valid models...")

try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    if available_models:
        st.success("✅ SUCCESS! The server found these valid models:")
        st.json(available_models)
        st.info("Copy one of the names above (e.g. 'models/gemini-pro') and put it in your app.py code.")
    else:
        st.error("⚠️ Connection made, but no models returned. Your API Key might be restricted.")

except Exception as e:
    st.error(f"❌ CRITICAL ERROR: {e}")
