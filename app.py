import streamlit as st
import google.generativeai as genai

# 1. CONFIGURE THE PAGE
st.set_page_config(page_title="RTCRO Prompt Engineer", page_icon="🤖")
st.title("🤖 Hybrid Meta-Prompting System")
st.caption("Powered by Google Gemini • RTCRO Framework")

# 2. SETUP API (Hidden from user)
# We will set the secret key in the hosting platform later
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key. Please configure it in Streamlit Secrets.")
    st.stop()

# 3. THE "BRAIN" (The System Instructions)
SYSTEM_INSTRUCTIONS = """
ROLE:
You are a Senior AI Prompt Architect. Your goal is to build the perfect "Meta-Prompt" using the RTCRO framework.

PROCESS:
PHASE 1: CONTEXT GATHERING
1. Analyze the user's request.
2. If vague, ask clarifying questions (Goal, Audience, Constraints).
3. Repeat until you have a Context Score of 90%+.

PHASE 2: RTCRO PIPELINE
Once context is saturated, execute:
[R]esearch best practices.
[T]emplate selection (CO-STAR for business, CRISPE for tech).
[C]ontext injection.
[R]eview for safety.
[O]ptimize for brevity.

OUTPUT:
Start final response with "🚀 HERE IS YOUR OPTIMIZED SYSTEM PROMPT:".
"""

# 4. INITIALIZE CHAT MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add the system instruction invisibly
    st.session_state.chat = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTIONS
    ).start_chat(history=[])

# 5. DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. HANDLE USER INPUT
if prompt := st.chat_input("Describe the prompt you need..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI Response
    try:
        response = st.session_state.chat.send_message(prompt)
        text_response = response.text
        
        # Show AI message
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
    except Exception as e:
        st.error(f"An error occurred: {e}")
