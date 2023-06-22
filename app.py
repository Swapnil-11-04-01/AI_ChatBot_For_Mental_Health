from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import streamlit as st
from streamlit_chat import message
import pygame


sound = True
pygame.mixer.init()
user_history = []

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Hello Chatbot")

config = ConfigurationManager()
base_config = config.get_base_config()
eve = Base(config=base_config)


ques_set_0 = eve.questions_0

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def generate_answer(key, value):
    if key == "name":
        user_message = st.session_state.input_text
        eve.user_name = user_message
        message_bot = value

    else:
        user_message = st.session_state.input_text
        message_bot = value

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})

for i, chat in enumerate(st.session_state.history):
    message(**chat, key=str(i)) #unpacking

c = 0
for key, value in ques_set_0.items():
    key = f"input_text_{c}"
    c+=1
    if key == "intro":
        message(value, key="intro")
    else:
        msg = st.text_input("Talk to the bot", key=key, on_change=generate_answer(key, value))
        user_history.append(msg)

for i, chat in enumerate(st.session_state.history):
    message(**chat, key=str(i)) #unpacking

