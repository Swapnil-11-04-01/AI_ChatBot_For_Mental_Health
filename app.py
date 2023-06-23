from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import chainlit as cl
from streamlit_chat import message
import pygame
import base64


config = ConfigurationManager()
base_config = config.get_base_config()
eve = Base(config=base_config)


ques_set_0 = eve.questions_0


sound = True
pygame.mixer.init()
pygame.mixer.music.load("templates/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)




user_history = []
counter = 0


@cl.on_message
async def generate_answer(message: str):
    global counter
    match counter:
        case 0:
            reply = eve.questions_0['intro']
            eve.speak(reply)
            counter += 1
        case 1:
            eve.user_name = message
            reply = eve.questions_0['name'] + ' ' + message
            eve.speak(reply)
            counter += 1
        case 2:
            reply = eve.questions_0['q1']
            eve.speak(reply)
            counter += 1
        case 3:
            reply = eve.questions_0['q2']
            eve.speak(reply)
            counter += 1
        case 4:
            reply = eve.questions_0['q3']
            eve.speak(reply)
            counter += 1
        case 5:
            reply = eve.questions_0['q4']
            eve.speak(reply)
            counter += 1
        case 6:
            reply = eve.questions_0['q5']
            eve.speak(reply)
            counter += 1
        case 7:
            reply = eve.questions_0['q6']
            eve.speak(reply)
            counter += 1
        case 8:
            reply = eve.questions_0['q7']
            eve.speak(reply)
            counter += 1
        case 9:
            reply = eve.questions_0['q8']
            eve.speak(reply)
            counter += 1
        case 10:
            reply = eve.questions_0['q9']
            eve.speak(reply)
            counter += 1

    await cl.Avatar(
        name="Tool 1",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()
    await cl.Message(
        content=str(counter) + ' ' + reply, author="Tool 1"
    ).send()
