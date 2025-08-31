import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("CHATBOT_API_URL")

st.set_page_config(page_title="Mental Wellbeing Chatbot", page_icon="💚", layout="wide")
st.markdown("<h1 style='text-align:center;'>💚 Mental Wellbeing</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#3CB371;'>Your personal stress & wellbeing assistant</h4>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

chat_container = st.container()

# Display chat history
def display_chat():
    with chat_container:
        for user_msg, bot_msg in st.session_state.history:
            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    background-color:#A8E6CF;
                    color:#000000;
                    padding:12px;
                    border-radius:15px;
                    margin-bottom:5px;
                    max-width:80%;
                    float:right;
                    clear:both;
                    word-wrap:break-word;">
                    <b>You:</b> {user_msg}
                </div>
                """,
                unsafe_allow_html=True
            )
            formatted_bot_msg = bot_msg.replace("\n", "<br>").replace("1.", "<br>1.")
            st.markdown(
                f"""
                <div style="
                    text-align:left;
                    background-color:#DCEFFF;
                    color:#000000;
                    padding:12px;
                    border-radius:15px;
                    margin-bottom:10px;
                    max-width:80%;
                    float:left;
                    word-wrap:break-word;">
                    <b>Bot:</b> {formatted_bot_msg}
                </div>
                """,
                unsafe_allow_html=True
            )

display_chat()


# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Ask anything...", key="user_input")
    send_button = st.form_submit_button("Send")

    if send_button and user_input:
        payload = {"sender": "user", "message": user_input}
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                bot_messages = response.json()
                bot_text = "\n".join([msg.get("text", "") for msg in bot_messages])
            else:
                bot_text = "Bot is offline."
        except Exception as e:
            bot_text = f"Error: {e}"

        st.session_state.history.append((user_input, bot_text))
        display_chat()
