from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import chainlit as cl
import matplotlib.pyplot as plt
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



def emotion_tracker():
    labels = ['Positivity', 'Negativity']
    values = [eve.positive, eve.negative]

    fig, ax = plt.subplots()

    ax.bar(labels, values, color=['green', 'blue'])

    ax.set_ylabel('Percentage')
    ax.set_title('Emotion Tracker')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()

    return fig

@cl.on_message
async def generate_answer(input: str):
    global counter
    match counter:
        case 0:
            reply = eve.questions_0['intro']
            eve.speak(reply)
            counter += 1
        case 1:
            eve.user_name = input
            reply = eve.questions_0['name'] + ' ' + input
            eve.speak(reply)
            counter += 1
        case 2:
            reply = eve.questions_0['q1']
            eve.speak(reply)
            preds, feel = eve.predict_(eve.vectorizer.transform(eve.preprocessor([input])))
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
        name="EVE Stage 1",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()

    await cl.Avatar(
        name="Emotional Tracker",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()

    await cl.Pyplot(name="Emotional State", figure=emotion_tracker(), display="side").send()
    await cl.Message(
        content="Your current Emotional State", author="Emotional Tracker"
    ).send()

    await cl.Message(
        content=reply, author="EVE Stage 1"
    ).send()
