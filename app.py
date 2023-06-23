from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import streamlit as st
from streamlit_chat import message
import pygame


sound = True
pygame.mixer.init()
user_history = []

# try:
#     pygame.mixer.music.stop()
# except:
#     pass

pygame.mixer.music.load("templates/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

config = ConfigurationManager()
base_config = config.get_base_config()
eve = Base(config=base_config)

ques_set_0 = eve.questions_0

if "history" not in st.session_state:
    st.session_state.history = []

st.title("EVE AI")

def generate_answer(msg):
    user_message = st.session_state.input_text
    message_bot = msg
    # eve.speak(message_bot)

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})

def reply(state=None):
    if state==1:
        pass
    else:
        msg = "hi"
        generate_answer(msg)

input_text = st.text_input("Talk to the bot", key="input_text", on_change=reply)
button = st.button("Submit")

if button:
    reply(state=1)

message("Hello")
for i, chat in enumerate(st.session_state.history):
    message(**chat, key=str(i)) #unpacking
