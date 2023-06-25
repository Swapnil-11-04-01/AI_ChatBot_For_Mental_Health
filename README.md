# Project 1 - EVE AI - ChatBot for Mental Health (Deployed) 💬🤖

**Duration:** September 2022 - June 2023

**Technologies used:** Python, Tkinter, Machine Learning, NLP, Chainlit, Docker, Github

## Project Description 📝

EVE AI is a chatbot designed to provide mental health support. The project utilizes various technologies and techniques to analyze user input and predict their mood. Here are the key features and components of the project:

1. EVE takes textual input from the user and performs sentiment analysis using Natural Language Processing (NLP) techniques.
2. Using the Catboost Classifier, EVE predicts the user's mood and provides the probability associated with the prediction.
3. EVE creates a dictionary with 7 mental states as keys and their representative vectors as values.
4. After a set of initial questions, EVE appends all the user's answers and measures cosine similarity with the 7 vectors representing the 7 different mental states.
5. Based on the cosine similarity, EVE identifies the closest mental state to the user's current state.
6. Once the mental state is identified, EVE asks more questions specifically related to that mental state.
7. At the end of the interaction, EVE plays an audio story to help the user feel better.

## Desktop App - EVE AI 💻🤖

EVE AI is implemented as a GUI-based desktop application using Python. The desktop app provides a user-friendly interface for interacting with the chatbot.

**Key Features:**
- Enhanced Virtual Emotional Artificial Intelligence (EVE AI)
- Voice-enabled AI

**Video Demonstration:** A video demonstration of the EVE AI desktop app can be found at [https://youtu.be/uxc6U1OCIo4](https://youtu.be/uxc6U1OCIo4).

**Deployed Web App:** The EVE AI web app is deployed and can be accessed at [https://eve-ai-hzpi.onrender.com/](https://eve-ai-hzpi.onrender.com/).