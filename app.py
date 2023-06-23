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
    print("SCORES: - ", eve.positive, eve.negative)
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
            feel = None
            preds = None
            probab=None
        case 1:
            eve.user_name = input
            reply = eve.questions_0['name'] + ' ' + input
            eve.speak(reply)
            counter += 1
            feel = None
            preds = None
            probab=None
        case 2:
            reply = eve.questions_0['q1']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 3:
            reply = eve.questions_0['q2']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 4:
            reply = eve.questions_0['q3']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 5:
            reply = eve.questions_0['q4']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 6:
            reply = eve.questions_0['q5']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 7:
            reply = eve.questions_0['q6']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 8:
            reply = eve.questions_0['q7']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 9:
            reply = eve.questions_0['q8']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)
        case 10:
            reply = eve.questions_0['q9']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            eve.speak(feel)
            eve.speak(reply)



    await cl.Avatar(
        name="EVE Stage 1 (feel)",
        url="https://img.icons8.com/?size=1x&id=JP608nHvU0ed&format=gif",
    ).send()

    await cl.Avatar(
        name="EVE Stage 1 (reply)",
        url="https://img.icons8.com/?size=1x&id=JP608nHvU0ed&format=gif",
    ).send()

    await cl.Avatar(
        name="Emotion",
        url="https://img.icons8.com/?size=1x&id=LEQaEe95xxN5&format=gif",
    ).send()

    await cl.Avatar(
        name="Emotional Tracker",
        url="https://img.icons8.com/?size=1x&id=oduDd8Uqz1ZX&format=gif",
    ).send()



    if probab and preds:
        text = f"{eve.emotion[preds]}: {round(probab*100, 2)}%"
        elements = [cl.Text(name="Emotion", content=text, display="inline")]
        await cl.Message(
            content="Emotion",
            author = "Emotion",
            elements=elements).send()

    fig = emotion_tracker()
    elements = [cl.Pyplot(name="Emotional State", figure=fig, display="side")]
    await cl.Message(
        content="Emotional State",
        author="Emotional Tracker",
        elements=elements
    ).send()



    if feel:
        await cl.Message(
            content=feel,
            author="EVE Stage 1 (feel)"
        ).send()

    await cl.Message(
        content=reply,
        author="EVE Stage 1 (reply)"
    ).send()
