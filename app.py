import streamlit as st
from streamlit_chat import message
import pygame

def typewriter_animation(text, delay=100):
    """
    Displays text one character at a time, with a delay between each character.

    Args:
        text (str): The text to display.
        delay (int): The delay between each character, in milliseconds.
    """
    for i, char in enumerate(text):
        st.write(char)
        pygame.time.wait(delay)

def generate_answer(msg):
    user_message = st.session_state.input_text
    message_bot = msg
    # eve.speak(message_bot)

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({"message": user_message, "is_user": True})
    typewriter_animation(message_bot)
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
