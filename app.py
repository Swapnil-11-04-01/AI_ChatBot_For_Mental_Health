from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import streamlit as st
from streamlit_chat import message
import pygame
import base64


class App:
    def __init__(self):
        st.set_page_config(page_title="EVE AI", page_icon=":bottts:", layout="wide", menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': 'Swapnil Sharma - https://swapnil-11-04-01.github.io/Personal-Portfolio/, '
                     'https://github.com/Swapnil-11-04-01'})
        st.title("EVE AI")
        self.sound = True
        pygame.mixer.init()

        self.user_history = []

        self.counter = 0

    def add_bg_from_local(self, image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string});
            background-size: cover;
            backdrop-filter: blur(0px);
        }}
                .stApp::before {{
                content: "";
                background-color: rgba(0, 0, 0, 0.15);
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: -1;
            }}
        </style>
        """,
            unsafe_allow_html=True
        )

    def music_player(self):
        pygame.mixer.music.load("templates/bg_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def generate_answer(self, msg):
        self.user_message = st.session_state.input_text
        self.message_bot = msg
        # eve.speak(message_bot)

        st.session_state.history.append({"message": self.user_message, "is_user": True})
        st.session_state.history.append({"message": self.message_bot, "is_user": False})
        st.session_state.input_text = ""


    def reply(self, state=None):
        msg = "hi\ngdf"
        self.generate_answer(msg)


    def main(self):
        self.config = ConfigurationManager()
        self.base_config = self.config.get_base_config()
        self.eve = Base(config=self.base_config)

        self.ques_set_0 = self.eve.questions_0

        if "history" not in st.session_state:
            st.session_state.history = []



        input_text = st.text_input("Talk to the bot", key="input_text", on_change=self.reply)

        message("Hello")
        for i, chat in enumerate(st.session_state.history):
            message(**chat, key=str(i)) #unpacking



if __name__ == "__main__":
    app = App()
    # app.add_bg_from_local('templates/wallpaper/bgimage.jpg')
    app.music_player()
    app.main()
