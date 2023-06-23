import pickle
import pyttsx3
from tqdm import tqdm
from pathlib import Path
import time
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from EVE_AI.entity.config_entity import BaseConfig
import warnings


warnings.filterwarnings("ignore")


class Base:
    def __init__(self, config: BaseConfig):
        self.intent_dict = {}
        self.config = config

        self.engine = pyttsx3.init('sapi5')
        self.rate = self.engine.getProperty('rate')
        self.voice = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voice[1].id)
        self.engine.setProperty('rate', self.rate * 0.86)

        self.intent_data = pd.read_csv(self.config.intent_data)
        self.preprocessor = pickle.load(open(self.config.base_preprocessor_path, "rb"))
        self.vectorizer = pickle.load(open(self.config.fitted_tokenizer_path, "rb"))
        self.distance_vector = pickle.load(open(self.config.distance_vector_path, "rb"))
        self.model = pickle.load(open(self.config.trained_model_path, "rb"))

        self.negative = 0.0
        self.positive = 0.0
        self.total_score = 0.0

        self.user_name = ""

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

        self.questions_0 = {
            "intro": "Hii! I'm EVE, an Enhanced Virtual Emotional Artificial Intelligence. Find me as your friend and a "
                "personal companion. Before we proceed, may I know your first name?",
            "name": "That's a nice name!. So, how are you doing",
            "q1": "Is there anything you want to talk about?",
            "q2": "How's your stress level lately",
            "q3": "Have you been eating and sleeping",
            "q4": "Would you be willing to talk to someone",
            "q5": "What would you like to achieve from our conversation?",
            "q6": "Can you tell me a bit about yourself and your background?",
            "q7": "What are some of the challenges or difficulties you've been facing recently?",
            "q8": "How have these challenges been impacting your daily life or overall well-being?",
            "q9": "Is there anything else you would like me to know?"
        }

        self.questions_1 = {"depression": ["How have you been feeling lately?",
                                         "Have you noticed any changes in your mood or energy levels?",
                                         "Are there any specific challenges or difficulties you're currently facing?",
                                         "Do you find it hard to find joy or interest in activities that used to bring you pleasure?",
                                         "Are there times when you feel a sense of sadness or emptiness that you can't quite explain?",
                                         "Have you noticed any changes in your sleep patterns or appetite?",
                                         "Are there any negative thoughts or self-critical beliefs that seem to dominate your thinking?",
                                         "Have you experienced a loss of motivation or difficulty concentrating on tasks?",
                                         "Have you tried any strategies or activities that have helped improve your mood in the past?",
                                         "Is there anything you'd like to discuss or explore further to support your emotional well-being?"],
                          "anxiety": ["How are you feeling right now?",
                                      "Is there anything on your mind that's causing you distress?",
                                      "Have you noticed any changes in your mood or emotions recently?",
                                      "Are there any specific situations or challenges that you're finding difficult to navigate?",
                                      "Do you find it hard to relax or find peace of mind at times?",
                                      "Are there certain thoughts or worries that seem to occupy your mind more than usual?",
                                      "Have you noticed any physical sensations that accompany your emotional state?",
                                      "Are there any particular areas of your life where you're feeling overwhelmed?",
                                      "Have you tried any strategies to manage stress or find balance when things feel challenging?",
                                      "Is there anything you'd like to talk about or explore further to help improve your well-being?"],
                          "paranoia": ["How have you been feeling lately?",
                                       "Have you noticed any changes in your thoughts or beliefs about others or the world around you?",
                                       "Are there specific situations or interactions that make you feel more suspicious or on edge?",
                                       "Do you find it difficult to trust others or believe their intentions?",
                                       "Are there times when you feel like you're being watched or monitored?",
                                       "Have you noticed any physical sensations, such as increased heart rate or heightened awareness, when you experience paranoia?",
                                       "Are there any specific thoughts or concerns that tend to occupy your mind and contribute to feelings of paranoia?",
                                       "Have you found any strategies or coping mechanisms that have helped you manage or alleviate paranoid thoughts in the past?",
                                       "Is there anyone you feel comfortable confiding in or discussing your concerns with?",
                                       "Is there anything specific you'd like to explore or discuss further to help address your experiences of paranoia?"],
                          "sleeping_disorder": ["How have you been sleeping lately?",
                                                "Have you noticed any changes in your sleep patterns or difficulties falling asleep or staying asleep?",
                                                "Are there any specific factors or concerns that you think might be affecting your sleep?",
                                                "Do you feel rested and rejuvenated after waking up, or do you often feel tired and fatigued?",
                                                "Are there any particular thoughts or worries that keep you awake at night?",
                                                "Have you tried any strategies or techniques to improve your sleep quality?",
                                                "Do you maintain a consistent sleep schedule, or do you have irregular sleep patterns?",
                                                "Have you noticed any physical or emotional symptoms that could be linked to your sleeping difficulties?",
                                                "Is there anything in your environment that might be impacting your sleep, such as noise, light, or temperature?",
                                                "Is there anything specific you'd like to discuss or explore further to help improve your sleep?"],
                          "substance_abuse": ["How have you been feeling lately?",
                                              "Have you noticed any changes in your substance use patterns or behaviors?",
                                              "Are there specific substances that you find yourself using more frequently or in larger amounts?",
                                              "Do you feel a strong urge or craving to use substances?",
                                              "Have you experienced any negative consequences or impacts on your life as a result of substance use?",
                                              "Are there specific triggers or situations that tend to lead to substance use?",
                                              "Have you tried any strategies or methods to reduce or control your substance use in the past?",
                                              "Is there anyone in your support network whom you feel comfortable discussing your concerns about substance abuse with?",
                                              "Are there any underlying emotional or psychological factors that you think might be contributing to your substance use?",
                                              "Is there anything specific you'd like to explore or discuss further to address your substance abuse concerns?"],
                          "personality_disorder": ["How have you been feeling lately?",
                                                   "Have you noticed any patterns in your thoughts, emotions, or behaviors that seem to repeat themselves?",
                                                   "Are there specific situations or interactions that tend to trigger difficulties or conflicts for you?",
                                                   "Do you find it challenging to maintain stable relationships or experience difficulties with interpersonal dynamics?",
                                                   "Are there any specific emotions or mood changes that you often struggle with?",
                                                   "Have you noticed any patterns of impulsive or risky behaviors?",
                                                   "Are there any particular coping mechanisms or strategies that have helped you manage your emotions or challenges in the past?",
                                                   "Is there anyone in your support network whom you feel comfortable discussing your concerns or difficulties related to your personality?"
                                                   "Have you explored any therapeutic interventions or techniques that have been beneficial for you?",
                                                   "Is there anything specific you'd like to discuss or explore further to support your well-being and manage the challenges associated with your personality?"],
                          "happy": ["How have you been feeling lately?",
                                                   "What are the things that bring you joy and happiness in your life?",
                                                   "Have you noticed any changes in your overall level of happiness or satisfaction?",
                                                   "Are there any specific areas of your life where you feel unhappy or dissatisfied?",
                                                   "What are some of the challenges or obstacles that you think might be impacting your happiness?",
                                                   "Are there any activities or hobbies that you used to enjoy but no longer find fulfilling?",
                                                   "Have you tried any strategies or techniques to improve your mood or overall happiness?",
                                                   "Is there anyone in your support network whom you feel comfortable discussing your happiness concerns with?",
                                                   "Are there any underlying factors or life events that you think might be influencing your happiness levels?",
                                                   "Is there anything specific you'd like to explore or discuss further to enhance your happiness and well-being?"]
                          }

        self.questions_2 = ["Do you have little interest or pleasure in doing things?",
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

    @staticmethod
    def save_model(path: Path, model):
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    @staticmethod
    def load_model(path: Path):
        with open(path, 'rb') as f:
            model = pickle.load(f)
        return model


    def speak(self, audio):
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
        return preds, probab, feel


    def intent_data_modifier(self, data):
        combined_intent_vector = []
        for col in tqdm(data.columns):
            self.intent_dict[col] = data[col].str.cat(sep=' ')
            combined_intent_vector.append(self.intent_dict[col])
        combined_intent_vector = pd.Series(combined_intent_vector).apply(self.preprocessor)
        self.vectorizer.fit(pd.Series(combined_intent_vector))
        for key, values in tqdm(self.intent_dict.items()):
            self.intent_dict[key] = self.vectorizer.transform([values])

        self.save_model(self.distance_vector, self.intent_dict)


    def intent(self, message):
        intent_dict = self.load_model(self.distance_vector)
        message = self.preprocessor(message)
        message = self.vectorizer.transform([message])
        vectors_array = [v.toarray().flatten() for v in intent_dict.values()]
        similarities = cosine_similarity(message.reshape(1, -1), vectors_array)
        closest_index = similarities.argmin()
        emotion = list(intent_dict.keys())[closest_index]
        return emotion

    def respond(self, message):
        emotion = self.intent(message)
        return self.questions_1[emotion]


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
            for sentence in self.questions_2:
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
