import time
import re
# import spacy
import pickle
import speech_recognition as sr
import pyttsx3
from colorama import Fore

# import EVE
# from EVE import startWindow

s = sr.Recognizer()

engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)


def speak(audio):
    engine.setProperty('rate', rate * 0.86)
    engine.say(audio)
    engine.runAndWait()


preprocessor = pickle.load(open("../../../artifacts/prepare_preprocessor/prepare_preprocessor.pkl", "rb"))
vectorizer = pickle.load(open("../../../artifacts/prepare_fitted_tokenizer/prepare_fitted_tokenizer.pkl", "rb"))
model = pickle.load(open("../../../artifacts/training/model.pkl", "rb"))

emotion = {
    0: "Sadness",
    1: "Happiness",
    2: "Love",
    3: "Anger",
    4: "Fear",
    5: "Surprise",
}

intents = {
    'hi': ['hello', 'hey', 'hi!', 'hi'],
    'bye': ['goodbye', 'buhbye', 'bye'],
    'depression': ['depressed', 'sad', 'worried', 'despair', 'misery', 'bad'],
    'anxiety': ['anxiety', 'anxious', 'nervous', 'stress', 'strain', 'tension', 'discomfort', 'tensed'],
    'paranoia': ['disbelieve', 'distrustful', 'doubting', 'incredulous', 'mistrustful', 'negativistic', 'questioning',
                 'show-me', 'skeptical', 'suspecting', 'suspicious', 'unbelieving'],
    'sleeping_disorder': ['restlessness', 'indisposition', 'sleeplessness', 'stress', 'tension', 'vigil', 'vigilance',
                          'wakefulness'],
    'substance_abuse': ['alcohol abuse', 'drug abuse', 'drug use', 'addiction', 'alcoholic addiction', 'alcoholism',
                        'chemical abuse', 'dipsomania', 'drug dependence', 'drug habit', 'narcotics abuse',
                        'solvent abuse'],
    'personality_disorder': ['insanity', 'mental disorder', 'schizophrenia', 'craziness', 'delusions', 'depression',
                             'derangement', 'disturbed mind', 'emotional disorder', 'emotional instability',
                             'loss of mind', 'lunacy', 'madness', 'maladjustment', 'mania', 'mental disease',
                             'mental sickness', 'nervous breakdown', 'nervous disorder',
                             'neurosis', 'neurotic disorder', 'paranoia', 'phobia', 'psychopathy', 'psychosis',
                             'sick mind', 'troubled mind', 'unbalanced mind', 'unsoundness of mind'],
    'happy': ['good', 'great', 'relieved', 'happy', 'okay']
}

responses = {
    'hi': 'Hello, i am a medical healthcare chatbot!',
    'bye': 'Thank you for your time!',
    'default': 'Sorry, i am not able to understand you'
}

dictionary = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0
}

s = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3
}

questions = ["Do you have little interest or pleasure in doing things?", "Feeling down, depressed, or hopeless",
             "Trouble falling or staying asleep, or sleeping too much", "Feeling tired or having little energy",
             "Feeling bad about yourself - or that you are a failure or have let yourself or your family down"]

# nlp = spacy.load("en_core_web_lg")


bot = "BOT: {0}"
user = "USER: {0}"

negative = 0.0
positive = 0.0
total_score = 0.0


def intent(message):
    for words in intents.keys():
        pattern = re.compile('|'.join([syn for syn in intents[words]]))
        match = pattern.search(message)
        if match:
            return words
    return 'default'


def respond(message):
    word = intent(message)
    return responses[word]


def score(name):
    sc = 0
    for k in dictionary.keys():
        sc += dictionary[k] * s[k]

    msg = f"Your mental assessment score is {sc}"
    # startWindow().greet().Insert_Message()
    # print(Fore.RED + "Your mental assessment score is ",sc)
    speak(msg)
    if (sc >= 0 and sc <= 9):
        print(Fore.RED + bot.format(
            "Please make sure that you keep checking in with me. What's your mood now after opening up?"))
        speak(bot.format("Please make sure that you keep checking in with me. What's your mood now after opening up?"))
        message = user.format(input(Fore.YELLOW)).lower()
        m_intent = intent(message)
        if (m_intent == 'depression'):
            depression(name)
        elif (m_intent == 'anxiety'):
            anxiety(name)
        elif (m_intent == 'sleeping disorder'):
            sleeping_disorder(name)
        elif (m_intent == 'paranoia'):
            paranoia(name)
        elif (m_intent == 'personality_disorder'):
            personality_disorder(name)
        elif (m_intent == substance_abuse):
            substance_abuse(name)
        elif (m_intent == 'happy'):
            time.sleep(1)
            print(Fore.RED + bot.format("Please ask me for help whenever you feel like it! I'm always online."))
        else:
            extreme(name)
    elif sc >= 10 and sc <= 15:
        extreme(name)


def extreme(name):
    print(Fore.RED + bot.format(
        "We\'re really sorry to know that and for further assistance we would try to connect you with our local assistance who is available 24/7"))
    speak(
        "We\'re really sorry to know that and for further assistance we would try to connect you with our local assistance who is available 24/7")
    time.sleep(1)
    print(Fore.RED + bot.format("Here are the details", name))
    print(Fore.RED + bot.format("Contact Jeevan Suicide Prevention Hotline"))
    print(
        Fore.RED + bot.format("Address:171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107"))
    print(Fore.RED + bot.format("Number : 044 2656 4444"))
    speak("Here are the details" + name +
          "Contact Jeevan Suicide Prevention Hotline" +
          "Address:171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107" +
          "Number : 044 2656 4444")


def quiz(name):
    time.sleep(1)
    print(Fore.RED + bot.format(
        "Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to evaluate your mental health"))
    speak(
        "Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to evaluate your mental health")
    print(Fore.RED)
    time.sleep(0.8)
    print(Fore.RED + bot.format("To respond please type the following answer depending upon your choice"))
    print(Fore.RED + "A. not at all")
    print(Fore.RED + "B. several days")
    print(Fore.RED + "C. more than half a day")
    print(Fore.RED + "D. all the days")
    print(Fore.RED)
    speak("To respond please type the following answer depending upon your choice. " +
          "A. not at all " +
          "B. several days " +
          "C. more than half a day " +
          "D. all the days ")
    time.sleep(1)
    print(Fore.RED + "Now we'll be starting with the quiz,type okay if you're ready!")
    speak("Now we'll be starting with the quiz, type 'okay' if you're ready!")
    inp = input(Fore.YELLOW).lower()
    if inp == 'okay':
        for sentence in questions:
            time.sleep(1)
            print(Fore.RED + bot.format(sentence))
            speak(sentence)
            resp = input(Fore.YELLOW).lower()
            dictionary[resp] = dictionary[resp] + 1

        print(Fore.RED)
        time.sleep(1)
        print(Fore.RED + "Thank you for taking the assessment!")
        speak("Thank you for taking the assessment!")
        for k in dictionary.keys():
            print(Fore.RED + k, dictionary[k])
        score(name)

    else:
        print(Fore.RED + "Thank you!")
        speak("Thank you!")


def predict_(x):
    x = preprocessor(x)
    tfidf = vectorizer.transform([x])
    preds = model.predict(tfidf)[0][0]
    probab = model.predict_proba(tfidf)[0][preds]
    print(preds, probab)
    if preds == 0 or preds == 3 or preds == 4:
        print(Fore.RED, emotion[preds], f"{round(probab, 2)*100}%")
    else:
        print(Fore.GREEN, emotion[preds], f"{round(probab, 2) * 100}%")
    feel = feeling(preds, probab)
    return preds, feel


def feeling(preds, probab):
    global negative, positive, total_score
    if preds == 0 or preds == 3 or preds == 4:
        negative = negative + probab
        print(Fore.WHITE, f"Positivity Score : {round(positive, 2)}")
        print(Fore.WHITE, f"Negativity Score : {round(negative, 2)}")
        total_score = positive - negative

        if total_score > 0:
            print(Fore.GREEN, f"Net Score : {round(total_score, 2)}")
        elif total_score < 0:
            print(Fore.RED, f"Net Score : {round(total_score, 2)}")
        else:
            print(Fore.YELLOW, f"Net Score : {round(total_score, 2)}")

        if probab >= 0.5:
            time.sleep(1)
            # print(Fore.RED + bot.format("Oh, sorry to hear that!"))
            # speak("Oh, sorry to hear that!")
            return "Oh, I am so sorry to hear that!"
        else:
            time.sleep(1)
            # print(Fore.RED + bot.format("Okay, thanks for sharing."))
            # speak("Okay, thanks for sharing.")
            return "Okay, thanks for sharing."
    else:

        positive = positive + probab
        print(Fore.WHITE, f"Positivity Score : {round(positive, 2)}")
        print(Fore.WHITE, f"Negativity Score : {round(negative, 2)}")
        total_score = positive - negative

        if total_score > 0:
            print(Fore.GREEN, f"Net Score : {round(total_score, 2)}")
        elif total_score < 0:
            print(Fore.RED, f"Net Score : {round(total_score, 2)}")
        else:
            print(Fore.YELLOW, f"Net Score : {round(total_score, 2)}")

        if probab >= 0.5:
            time.sleep(1)
            # print(Fore.RED + bot.format("That's great to hear!"))
            # speak("That's great to hear!")
            return "Wow!! That's great to hear!"
        else:
            time.sleep(1)
            # print(Fore.RED + bot.format("Okay, thanks for sharing."))
            # speak("Okay, thanks for sharing.")
            return "Okay, thanks for sharing."


def classification(pred):
    if pred == 0 or pred == 3 or pred == 4:
        return 0
    else:
        return 1


# def name_extraction(message):
#     doc = nlp(message)
#     name = ''
#     for ent in doc.ents:
#         if ent.label_=="PERSON":
#             return str(ent)
#     x = message.split()
#     if len(x)<=2:
#         return (x[0])
#     elif (' '.join(x[0:3]).lower())=='my name is':
#         return ''.join(x[3:])

def cbt():
    time.sleep(1)
    print(Fore.RED + bot.format(
        "Mood tracking and thinking hygiene - among other useful concepts - are skills you'll learn as you practice CBT"))
    speak(
        "Mood tracking and thinking hygiene - among other useful concepts - are skills you'll learn as you practice CBT")
    time.sleep(1)
    print(Fore.RED + bot.format(
        "Skills that can help you make positive changes to your thoughts, feelings and behaviour"))
    speak("Skills that can help you make positive changes to your thoughts, feelings and behaviour")


def depression(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        'There you go...let it all slide out.Unhappiness cannot stick in a person\'s soul when it\'s slick with tear.'))
    speak(
        'There you go...let it all slide out.Unhappiness cannot stick in a person\'s soul when it\'s slick with tear.')


def anxiety(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        'Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.'))
    speak('Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.')


def paranoia(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        'If you want someone, you have to be willing to wait for them and trust that what you have is real and strong enough for them to wait for you. If somebody jumps ship for you, that fact will always haunt you because you\'ll know they\'re light on their feet. Spare yourself the paranoia and the pain and walk away until the coast is clear.'))
    speak(
        'If you want someone, you have to be willing to wait for them and trust that what you have is real and strong enough for them to wait for you. If somebody jumps ship for you, that fact will always haunt you because you\'ll know they\'re light on their feet. Spare yourself the paranoia and the pain and walk away until the coast is clear.')


def sleeping_disorder(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        'Overhead, the glass envelope of the Insomnia Balloon is malfunctioning. It blinks on and off at arrhythmic intervals, making the world go gray:black, gray:black. In the distance, a knot of twisted trees flashes like cerebral circuitry.'))
    speak(
        'Overhead, the glass envelope of the Insomnia Balloon is malfunctioning. It blinks on and off at arrhythmic intervals, making the world go gray:black, gray:black. In the distance, a knot of twisted trees flashes like cerebral circuitry.')


def personality_disorder(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        '...repeated trauma in childhood forms and deforms the personality. The child trapped in an abusive environment is faced with formidable tasks of adaptation. She must find a way to preserve a sense of trust in people who are untrustworthy, safety in a situation that is unsafe, control in a situation that is terrifyingly unpredictable, power in a situation of helplessness. Unable to care for or protect herself, she must compensate for the failures of adult care and protection with the only means at her disposal, an immature system of psychological defenses.'))
    speak(
        '...repeated trauma in childhood forms and deforms the personality. The child trapped in an abusive environment is faced with formidable tasks of adaptation. She must find a way to preserve a sense of trust in people who are untrustworthy, safety in a situation that is unsafe, control in a situation that is terrifyingly unpredictable, power in a situation of helplessness. Unable to care for or protect herself, she must compensate for the failures of adult care and protection with the only means at her disposal, an immature system of psychological defenses.')


def substance_abuse(name):
    time.sleep(1)
    print(Fore.RED + bot.format('Gosh, that is tough'))
    speak('Gosh, that is tough')
    time.sleep(1)
    print(Fore.RED + bot.format('I am sorry to hear that,'), name)
    speak('I am sorry to hear that,' + name)
    time.sleep(1)
    print(Fore.RED + bot.format('Here is a thought that might motivate you!'))
    speak('Here is a thought that might motivate you!')
    time.sleep(1)
    print(Fore.RED + bot.format(
        ' My Recovery Must Come First So That Everything I Love In Life Doesn’t Have To Come Last.'))
    speak(' My Recovery Must Come First So That Everything I Love In Life Doesn’t Have To Come Last.')
