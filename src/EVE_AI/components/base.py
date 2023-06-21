import pickle
import pyttsx3
import re
import time
from pathlib import Path
import pandas as pd
import re
from nltk.stem import PorterStemmer
from EVE_AI.entity.config_entity import BaseConfig
import warnings

warnings.filterwarnings("ignore")


class Base:
    def __init__(self, config: BaseConfig):
        self.config = config

        self.engine = pyttsx3.init('sapi5')
        self.rate = self.engine.getProperty('rate')
        self.voice = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voice[1].id)

        self.intent_data = pd.read_csv(self.config.root_data_dir, header=True)
        self.preprocessor = pickle.load(open(self.config.base_preprocessor_path, "rb"))
        self.vectorizer = pickle.load(open(self.config.base_tokenizer_path, "rb"))
        self.model = pickle.load(open(self.config.base_model_path, "rb"))

        self.negative = 0.0
        self.positive = 0.0
        self.total_score = 0.0

        self.emotion = {
            0: "Sadness",
            1: "Happiness",
            2: "Love",
            3: "Anger",
            4: "Fear",
            5: "Surprise",
        }

        self.intents = {
            'depression': [],
            'anxiety': [],
            'paranoia': [],
            'sleeping_disorder': [],
            'substance_abuse': [],
            'personality_disorder': [],
            'happy': []
        }

        self.responses = {}

        self.questions = ["Do you have little interest or pleasure in doing things?",
                          "Feeling down, depressed, or hopeless",
                          "Trouble falling or staying asleep, or sleeping too much",
                          "Feeling tired or having little energy",
                          "Feeling bad about yourself - or that you are a failure or have let yourself or your family down"]

        self.dictionary = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0
        }

        self.s = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3
        }

    def speak(self, audio, rate):
        self.engine.setProperty('rate', rate * 0.86)
        self.engine.say(audio)
        self.engine.runAndWait()


    def feeling(self, preds, probab):
        if preds == 0 or preds == 3 or preds == 4:
            self.negative = self.negative + probab
            print(f"Positivity Score : {round(self.positive, 2)}")
            print(f"Negativity Score : {round(self.negative, 2)}")
            self.total_score = self.positive - self.negative

            if self.total_score > 0:
                print(f"Net Score : {round(self.total_score, 2)}")
            elif self.total_score < 0:
                print(f"Net Score : {round(self.total_score, 2)}")
            else:
                print(f"Net Score : {round(self.total_score, 2)}")

            if probab >= 0.5:
                time.sleep(1)
                return "Oh, I am so sorry to hear that!"
            else:
                time.sleep(1)
                return "Okay, thanks for sharing."

        else:
            self.positive = self.positive + probab
            print(f"Positivity Score : {round(self.positive, 2)}")
            print(f"Negativity Score : {round(self.negative, 2)}")
            self.total_score = self.positive - self.negative

            if self.total_score > 0:
                print(f"Net Score : {round(self.total_score, 2)}")
            elif self.total_score < 0:
                print(f"Net Score : {round(self.total_score, 2)}")
            else:
                print(f"Net Score : {round(self.total_score, 2)}")

            if probab >= 0.5:
                time.sleep(1)
                return "Wow!! That's great to hear!"
            else:
                time.sleep(1)
                return "Okay, thanks for sharing."

    def predict_(self, x):
        x = self.preprocessor(x)
        tfidf = self.vectorizer.transform([x])
        preds = self.model.predict(tfidf)[0][0]
        probab = self.model.predict_proba(tfidf)[0][preds]
        print(preds, probab)
        if preds == 0 or preds == 3 or preds == 4:
            print(self.emotion[preds], f"{round(probab, 2) * 100}%")
        else:
            print(self.emotion[preds], f"{round(probab, 2) * 100}%")
        feel = self.feeling(preds, probab)
        return preds, feel


    def intent(self, message):
        for words in self.intents.keys():
            pattern = re.compile('|'.join([syn for syn in self.intents[words]]))
            match = pattern.search(message)
            if match:
                return words
        return 'default'

    def respond(self, message):
        word = self.intent(message)
        return self.responses[word]


    def quiz(self, name):
        time.sleep(1)
        self. speak("Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to "
              "evaluate your mental health")

        time.sleep(0.8)
        self.speak("To respond please type the following answer depending upon your choice. " +
              "A. not at all " +
              "B. several days " +
              "C. more than half a day " +
              "D. all the days ")

        time.sleep(1)
        self.speak("Now we'll be starting with the quiz, type 'okay' if you're ready!")

        inp = input().lower()
        if inp == 'okay':
            for sentence in self.questions:
                time.sleep(1)
                self.speak(sentence)
                resp = input().lower()
                self.dictionary[resp] = self.dictionary[resp] + 1

            time.sleep(1)
            self.speak("Thank you for taking the assessment!")

            self.score(name)

        else:
            self.speak("Thank you!")

    def score(self, name):
        sc = 0
        for k in self.dictionary.keys():
            sc += self.dictionary[k] * self.s[k]

        msg = f"Your mental assessment score is {sc}"
        self.speak(msg)

        if 0 <= sc <= 9:
            self.speak("Please make sure that you keep checking in with me. What's your mood now after opening up?")
            message = input()
            m_intent = self.intent(message)
            if m_intent == 'depression':
                self.depression(name)
            elif m_intent == 'anxiety':
                self.anxiety(name)
            elif m_intent == 'sleeping disorder':
                self.sleeping_disorder(name)
            elif m_intent == 'paranoia':
                self.paranoia(name)
            elif m_intent == 'personality_disorder':
                self.personality_disorder(name)
            elif m_intent == 'substance_abuse':
                self.substance_abuse(name)
            elif m_intent == 'happy':
                time.sleep(1)
                print("Please ask me for help whenever you feel like it! I'm always online.")
            else:
                self.extreme(name)
        elif 10 <= sc <= 15:
            self.extreme(name)

    def extreme(self, name):
        self.speak("We\'re really sorry to know that and for further assistance we would try to connect you with our local "
              "assistance who is available 24/7")
        time.sleep(1)

        self.speak("Here are the details" + name +
              "Contact Jeevan Suicide Prevention Hotline" +
              "Address:171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107" +
              "Number : 044 2656 4444")

    def depression(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(
            'There you go...let it all slide out.Unhappiness cannot stick in a person\'s soul when it\'s slick with tear.')

    def anxiety(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(
            'Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.')

    def paranoia(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(
            'If you want someone, you have to be willing to wait for them and trust that what you have is real and strong enough for them to wait for you. If somebody jumps ship for you, that fact will always haunt you because you\'ll know they\'re light on their feet. Spare yourself the paranoia and the pain and walk away until the coast is clear.')

    def sleeping_disorder(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(
            'Overhead, the glass envelope of the Insomnia Balloon is malfunctioning. It blinks on and off at arrhythmic intervals, making the world go gray:black, gray:black. In the distance, a knot of twisted trees flashes like cerebral circuitry.')

    def personality_disorder(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(
            '...repeated trauma in childhood forms and deforms the personality. The child trapped in an abusive environment is faced with formidable tasks of adaptation. She must find a way to preserve a sense of trust in people who are untrustworthy, safety in a situation that is unsafe, control in a situation that is terrifyingly unpredictable, power in a situation of helplessness. Unable to care for or protect herself, she must compensate for the failures of adult care and protection with the only means at her disposal, an immature system of psychological defenses.')

    def substance_abuse(self, name):
        time.sleep(1)
        self.speak('Gosh, that is tough')
        time.sleep(1)
        self.speak('I am sorry to hear that,' + name)
        time.sleep(1)
        self.speak('Here is a thought that might motivate you!')
        time.sleep(1)
        self.speak(' My Recovery Must Come First So That Everything I Love In Life Doesn’t Have To Come Last.')
