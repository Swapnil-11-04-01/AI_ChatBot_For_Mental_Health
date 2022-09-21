import base
import time


# print(base.Fore.RED + base.bot.format("Hello human, I am Eve, you can have me as your personal companion, may I know your name?\n"))
# base.speak("Hello human, I am Eve, you can have me as your personal companion, may I know your name?")


def greet():
    while True:
        time.sleep(1)
        base.negative = 0
        base.positive = 0
        print(base.Fore.RED + base.bot.format('Hi! I\'m a medical healthcare chatbot, EVE!'))
        base.speak('Hi! I\'m a medical healthcare chatbot!, EVE')
        time.sleep(1)
        print(base.Fore.RED + base.bot.format('Before we proceed, may I know your first name?'))
        base.speak('Before we proceed, may I know your first name?')
        message = input(base.Fore.YELLOW)
        # name = base.name_extraction(message)
        name = message
        time.sleep(1)
        print(base.Fore.RED + base.bot.format(name), ", That's a nice name!")
        base.speak(name + ", That's a nice name!")
        time.sleep(1)
        print(base.Fore.RED + base.bot.format("Before we get started, I want to know about your current mood"))
        base.speak("Before we get started, I want to know about your current mood")
        message = input(base.Fore.YELLOW).lower()
        sentiment = base.predict_(message)
        time.sleep(1)
        print(base.Fore.RED + base.bot.format("So"), name, "I'm a CBT coach that can consult with during difficult times, and also not-so-difficult times. Do you wanna know a little more?")
        base.speak("So" + name + "I'm a CBT coach that can consult with during difficult times, and also not-so-difficult times. Do you wanna know a little more?")
        time.sleep(1)
        message = input(base.Fore.YELLOW).lower()
        sentiment = base.predict_(message)
        pos = base.classification(sentiment)
        if pos == 1:
            base.cbt()
        print(base.Fore.RED + base.bot.format(name), ",can you walk me through how did your last week go?")
        base.speak(name + ",can you walk me through how did your last week go?")
        time.sleep(1)
        message = input(base.Fore.YELLOW).lower()
        sentiment = base.predict_(message)
        pos = base.classification(sentiment)
        if pos == 0:
            time.sleep(1)
            print(base.Fore.RED + base.bot.format(name), "I know that question can be tough and sometime painful to answer so I really appreciate you doing it")
            base.speak(name + "I know that question can be tough and sometime painful to answer so I really appreciate you doing it")
        time.sleep(1)
        print(base.Fore.RED + base.bot.format("Can you tell me a bit about what's going on in your life that has brought you here today?"))
        base.speak("Can you tell me a bit about what's going on in your life that has brought you here today?")
        message = input(base.Fore.YELLOW).lower()
        sentiment = base.predict_(message)
        if (base.negative == 0):
            time.sleep(1)
            print(base.Fore.RED + base.bot.format("That's awesome! You are showing improvement!"))
            base.speak("That's awesome! You are showing improvement!")
            time.sleep(1)
        else:
            time.sleep(1)
            print(base.Fore.RED + base.bot.format('I have got great tools for people dealing with stress,wanna give it a go,Yes/No?'))
            base.speak('I have got great tools for people dealing with stress,wanna give it a go?')
            time.sleep(1)
            message = input(base.Fore.YELLOW).lower()
            if message == 'yes':
                print(base.Fore.RED + base.bot.format("Great! Thanks for trusting me", name))
                base.speak("Great! Thanks for trusting me" + name)
                time.sleep(1)
                print(base.Fore.RED + base.bot.format("Let's start with a small mental assessment test,so buckle up!"))
                base.speak("Let's start with a small mental assessment test,so buckle up!")
                time.sleep(1)
                base.quiz(name)
            else:
                time.sleep(1)
                print(base.Fore.RED + base.bot.format("Please ask me for help whenever you feel like it! I'm always online."))
                base.speak("Please ask me for help whenever you feel like it! I'm always online.")

        print(base.Fore.RED + base.bot.format("Type 'Yes' to retake assessment, 'No' to exit"))
        base.speak("Type 'Yes' to retake assessment, 'No' to exit")
        retake = input(base.Fore.YELLOW).lower()

        if retake == 'no':
            break

greet()