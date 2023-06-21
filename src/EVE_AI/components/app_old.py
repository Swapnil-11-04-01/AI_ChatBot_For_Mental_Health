from tkinter import *
import pygame
from base import speak, predict_, total_score
import time
from colorama import Fore








sound = True
# Importing and handling sound
pygame.mixer.init()



def get_response(msg, step):
    match step:
        case 0:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "Is there anything you want to talk about?"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 1:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "How's your stress level lately"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 2:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "Have you been eating and sleeping"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 3:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "Would you be willing to talk to someone"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 4:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "What can I do for you"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 5:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "When is the best time to check in with you again?"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 6:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            ques = "Is there anything you want to talk about?"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, ques
        case 7:
            print(Fore.WHITE, f"\n\nStep : {startWindow.step}")
            last_msg = f"Please ask me for help whenever you feel like it! I'm always online. Also, before going, there is one surprise for you!! hahaha!! Until next time {startWindow.name}. Stay Happy, Keep Smiling"
            startWindow.step += 1
            sentiment, feel = predict_(msg)
            return feel, last_msg
        case 8:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../../../templates/Story_1.mp3")
            pygame.mixer.music.play(0)










class startWindow():
    name = "You"
    step = 0

    def __init__(self):
        self.root = Tk()
        self._setup_main_window()

    def run(self):
        self.root.mainloop()



    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self.insert(msg)

    def insert(self, msg):
        self.insert_message(msg)
        self.insert_response(msg)

    def insert_message(self, msg):
        if not msg:
            return
        self.EVE.config(fg="dark green")
        self.msg_entry.delete(0, END)
        msg1 = f"{startWindow.name}: {msg}\n\n"
        self.EVE.configure(state=NORMAL)
        self.EVE.insert(END, msg1)
        self.EVE.configure(state=DISABLED)
        self.EVE.see(END)

    def insert_response(self, msg):
        if not msg:
            return
        self.EVE.config(fg="red")
        self.msg_entry.delete(0, END)

        response = get_response(msg, startWindow.step)
        for _ in response:
            msg2 = f"EVE: {_}\n\n"
            self.EVE.configure(state=NORMAL)
            self.EVE.insert(END, msg2)
            speak(_)
            time.sleep(1)

        if startWindow.step == 8:
            # print("\n\n")
            # if total_score>0:
            #     print(Fore.GREEN, f"Final Score: {round(total_score, 2)} => Positive Mood")
            # elif total_score<0:
            #     print(Fore.RED, f"Final Score: {round(total_score, 2)} => Negative Mood")
            # else:
            #     print(Fore.YELLOW, f"Final Score: {round(total_score, 2)} => Neutral Mood")

            get_response(msg, startWindow.step)

        self.EVE.configure(state=DISABLED)
        self.EVE.see(END)



    def _setup_main_window(self):
        self.root.title("E.V.E AI - Your Personal Companion")
        self.root.state("zoomed")
        # self.root.resizable(False, False)

        # Background image
        self.img = PhotoImage(file="../../../templates/bgimage.png")
        self.label = Label(self.root, image=self.img)
        self.label.place(x=0, y=0)

        self.button1 = Button(self.label, text="START", fg="black", font=("Arial", 15), width=20, height=3, bg="violet", command=lambda: self.start(None))
        self.button1.place(relx=0.5, rely=0.5, anchor=CENTER)

    def start(self, event):
        try:
            pygame.mixer.music.stop()
        except:
            pass

        pygame.mixer.music.load("../../../templates/bg_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        startWindow.step = 0
        try:
            self.button1.destroy()
            self.EVE.destroy()
            self.bottom_label.destroy()
        except:
            pass

        msg = "Hii! I'm EVE, an Enhanced Virtual Emotional Artificial Intelligence. Find me as your friend and a personal companion. Before we proceed, may I know your first name?"
        speak(msg)

        # Central Frame
        self.Frame_label = Label(self.label, width=70, height=13, bg="dark blue")
        self.Frame_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Name Label
        name_label = Label(self.Frame_label, text = "Please Enter Your First Name Below", bg="dark blue", fg="white", font = ("Arial", 20))
        name_label.place(relwidth=1, relheight=0.5, rely=0, relx=0)

        # Input name
        self.name_input = Entry(self.Frame_label, bg="sky blue", fg="Dark Green", font = ("Arial", 15), justify=CENTER)
        self.name_input.place(relwidth=1, relheight=0.3, rely=0.5, relx=0)
        self.name_input.focus()
        self.name_input.bind("<Return>", self.enter_name)

        # start button
        start_button = Button(self.Frame_label, text="SUBMIT", fg="black", font=("Arial", 15), width=20, bg="violet", command=lambda: self.enter_name(None))
        start_button.place(relx=0, rely=0.8, relheight=.2, relwidth=1)

    def enter_name(self, event):
        startWindow.name = self.name_input.get()
        msg = f"{startWindow.name}, That's a nice name!. So, how are you doing {startWindow.name}?"
        speak(msg)
        self.chat()

    def chat(self):
        # Destroying Frame_label
        self.Frame_label.destroy()

        # Handling all widgets
        self.EVE = Text(self.root, height=60, width=50, relief=RIDGE, borderwidth=5, bg="pink", font=25)
        self.EVE.pack(side=LEFT, padx=5, pady=5)

        # scroll bar
        scrollbar = Scrollbar(self.EVE)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.EVE.yview)

        # bottom label
        self.bottom_label = Label(self.root, bg="dark blue", height=4)
        self.bottom_label.place(relwidth=1, rely=0.94)

        # Message entry
        self.msg_entry = Entry(self.bottom_label, bg="sky blue", fg="Dark Green", font=35)
        self.msg_entry.place(relwidth=0.79, relheight=0.7, rely=0.15, relx=0.003)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(self.bottom_label, text="SEND", fg="black", font=("Arial", 15), width=20, bg="violet", command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.8, rely=0.1, relheight=0.8, relwidth=0.10)

        # reset button
        send_button = Button(self.bottom_label, text="RESET", fg="black", font=("Arial", 15), width=20, bg="violet", command=lambda: self.start(None))
        send_button.place(relx=0.9, rely=0.1, relheight=0.8, relwidth=0.10)








# START
if __name__ == "__main__":
    app = startWindow()
    app.run()
