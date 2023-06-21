import streamlit as st
from streamlit_chat import message

message("My message")
message("Hello bot!", is_user=True)  # align's the message to the right

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust the speech rate (optional)
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Text-to-Speech Demo")
    text_input = st.text_input("Enter the text to be spoken")
    if st.button("Speak"):
        speak(text_input)

if __name__ == "__main__":
    main()