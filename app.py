from EVE_AI.components.base import Base
from EVE_AI.config.configuration import ConfigurationManager
import chainlit as cl
import matplotlib.pyplot as plt
import pygame
import numpy as np



config = ConfigurationManager()
base_config = config.get_base_config()
eve = Base(config=base_config)



ques_set_0 = eve.questions_0
ques_set_1 = eve.questions_1
ques_set_2 = eve.questions_2



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


def problem_tracker():
    labels = ['Anxiety', 'Depression', 'Paranoia', "Sleeping Disorder", "Substance Abuse", "Personality Disorder",
              "Happy"]
    values = [1-i[0] for i in eve.similarities.tolist()]
    # Determine the lower and higher values
    lower_value = min(values)
    higher_value = max(values)

    # Calculate the desired y-limits
    lower_limit = lower_value * 0.8
    higher_limit = higher_value * 1.5

    # Create the x-axis values
    x = np.arange(len(values))

    fig, ax = plt.subplots()

    ax.bar(labels, values, color=['red', 'yellow', 'orange', 'green', 'blue', 'brown', 'pink'])

    ax.set_ylabel('Score')
    ax.set_title('Mental State Tracker')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set the y-limits
    plt.ylim(lower_limit, higher_limit)

    plt.xticks(rotation=45)

    fig.tight_layout()

    return fig



@cl.on_message
async def generate_answer(input: str):
    global counter
    feel, preds, probab, eve.problem = None, None, None, None
    match counter:
        case 0:
            reply = ques_set_0['intro']
            eve.speak(reply)
            counter += 1
        case 1:
            eve.user_name = input
            reply = ques_set_0['name'] + ' ' + input
            eve.speak(reply)
            counter += 1
        case 2:
            reply = ques_set_0['q1']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 3:
            reply = ques_set_0['q2']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 4:
            reply = ques_set_0['q3']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 5:
            reply = ques_set_0['q4']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 6:
            reply = ques_set_0['q5']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 7:
            reply = ques_set_0['q6']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 8:
            reply = ques_set_0['q7']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 9:
            reply = ques_set_0['q8']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 10:
            reply = ques_set_0['q9']
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 11:
            reply = f"It's alright {eve.user_name}, feel free to share anything you want. So, {ques_set_1[eve.problem][0]}"
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.problem = eve.respond(" ".join(user_history))
            eve.speak(feel)
            eve.speak(reply)
        case 13:
            reply = ques_set_1[eve.problem][1]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 14:
            reply = ques_set_1[eve.problem][2]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 15:
            reply = ques_set_1[eve.problem][3]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 16:
            reply = ques_set_1[eve.problem][4]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 17:
            reply = ques_set_1[eve.problem][5]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 18:
            reply = ques_set_1[eve.problem][6]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 19:
            reply = ques_set_1[eve.problem][7]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 20:
            reply = ques_set_1[eve.problem][8]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 21:
            reply = ques_set_1[eve.problem][9]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 22:
            reply = ques_set_1[eve.problem][9]
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.speak(reply)
        case 23:
            preds, probab, feel = eve.predict_(input)
            counter += 1
            user_history.append(input)
            eve.speak(feel)
            eve.problem = eve.respond(" ".join(user_history))






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

    await cl.Avatar(
        name="Problem",
        url="https://icons8.com/icon/in2IMUCImGjB/disappointed",
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





    if eve.problem:
        text = f"Signs of {eve.problem} seen"
        elements = [cl.Text(name="Problem", content=text, display="inline")]
        await cl.Message(
            content="Problem",
            author = "Problem",
            elements=elements).send()

        fig = problem_tracker()
        elements = [cl.Pyplot(name="Mental State", figure=fig, display="side")]
        await cl.Message(
            content="Mental State",
            author="Emotional Tracker",
            elements=elements
        ).send()





    if feel:
        await cl.Message(
            content=feel,
            author="EVE Stage 1 (feel)"
        ).send()

    if reply:
        await cl.Message(
            content=reply,
            author="EVE Stage 1 (reply)"
        ).send()
