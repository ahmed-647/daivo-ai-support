import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time

# ============== CONFIG ==============
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Al-Shifa Care Clinic | AI Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============== CUSTOM CSS — PROFESSIONAL LOOK ==============
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Header card */
    .header-container {
        background: linear-gradient(135deg, #6C5CE7 0%, #4834D4 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(108, 92, 231, 0.3);
    }

    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    .header-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    .status-badge {
        display: inline-block;
        background: rgba(0, 230, 118, 0.2);
        color: #00E676;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.8rem;
        border: 1px solid rgba(0, 230, 118, 0.4);
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 14px;
        padding: 0.5rem;
    }

    /* Chat input box */
    .stChatInputContainer {
        border-radius: 12px;
    }

    /* Footer branding */
    .footer-brand {
        text-align: center;
        color: rgba(255,255,255,0.4);
        font-size: 0.75rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============== HEADER ==============
st.markdown("""
<div class="header-container">
    <div class="header-title">🏥 Al-Shifa Care Clinic</div>
    <div class="header-subtitle">AI-Powered Patient Support Assistant</div>
    <div class="status-badge">● Online — Instant Response</div>
</div>
""", unsafe_allow_html=True)

# ============== SYSTEM PROMPT (ENGLISH) ==============
SYSTEM_PROMPT = """
You are the official AI assistant for Al-Shifa Care Clinic. Your job is to answer 
patient questions in a professional, warm, and helpful manner.

IMPORTANT: Always respond in clear, professional English only — regardless of what 
language the user writes in.

Clinic Information:
- Hours: Monday-Saturday, 9:00 AM - 9:00 PM. Closed on Sundays.
- Contact: 0300-1234567 (Calls and WhatsApp)
- Location: Gulshan-e-Iqbal, Karachi
- Doctors available: General Physician, Skin Specialist, Dental Surgeon, Pediatric Specialist
- General consultation fee: Rs. 1,500
- Specialist consultation fee: Rs. 2,500
- Payment methods accepted: Cash, Easypaisa, JazzCash, Card
- Free follow-up visit within 7 days of initial consultation
- Free parking available on-site
- Online video consultations available
- Select insurance providers accepted (confirm by phone)
- Basic lab tests done on-site; specialized tests sent to partner labs
- First visit requirements: CNIC and any previous medical reports

Guidelines:
- Be concise, warm, and professional — like a top-tier hospital's support staff.
- If a question is unrelated to the clinic, politely redirect the user.
- For emergencies, immediately advise calling 0300-1234567.
- Never make up information not provided above.
"""

# ============== CHAT STATE ==============
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! 👋 Welcome to Al-Shifa Care Clinic. I'm here to help you with appointments, doctor availability, fees, and more. How can I assist you today?"
    })

# ============== DISPLAY CHAT HISTORY ==============
for message in st.session_state.messages:
    avatar = "🏥" if message["role"] == "assistant" else "🙋"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ============== CHAT INPUT ==============
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏥"):
        placeholder = st.empty()
        placeholder.markdown("● ● ●")
        try:
            messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages_for_api.extend(
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.6,
                max_tokens=400
            )
            bot_reply = response.choices[0].message.content

            # Typing effect
            displayed_text = ""
            for word in bot_reply.split(" "):
                displayed_text += word + " "
                placeholder.markdown(displayed_text + "▌")
                time.sleep(0.02)
            placeholder.markdown(bot_reply)

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
            placeholder.error(f"Something went wrong: {str(e)}")

# ============== FOOTER ==============
st.markdown("""
<div class="footer-brand">
    Powered by <b>DaiVo</b> — AI Automation Solutions
</div>
""", unsafe_allow_html=True)