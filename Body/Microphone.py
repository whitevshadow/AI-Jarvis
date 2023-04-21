import threading

import speech_recognition as sr
from googletrans import Translator
from playsound import playsound as play
from Body.Hotword import jarvis_dect


def Speech_On():
    try:
        path = 'Sounds\\Speech On.wav'
        play(path)
    except:
        path1 = 'Body\\Sounds\\Speech On.wav'
        play(path1)


def Speech_Off():
    try:
        path = 'Sounds\\Speech Off.wav'
        play(path)
    except:
        path1 = 'Body\\Sounds\\Speech Off.wav'
        play(path1)


def NonUnderstandable():
    try:
        path = 'Sounds\\Speech Misrecognition.wav'
        play(path)
    except:
        path1 = 'Body\\Sounds\\Speech Misrecognition.wav'
        play(path1)


def Listen():
    threading.Thread(target=Speech_On).start()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 0)
        try:
            print("Recognizing...")
            sentences = r.recognize_google(audio, language='en-in')
            threading.Thread(target=Speech_Off).start()
        except sr.UnknownValueError:
            threading.Thread(target=NonUnderstandable).start()
        except Exception as e:
            print(e)
            return ""
        return sentences


def ToEnglish(audio):
    if len(audio) > 3:
        Translate = Translator()
        Sent = Translate.translate(audio)
        text = Sent.text
        return text
    elif "None" in audio:
        print("Could not Understand")
    else:
        pass


def MicExecution():
    try:
        jarvis_dect()
        sentences = Listen()
        sentence = ToEnglish(sentences)
        print(f">> You : {sentences}")
        return sentence
    except UnboundLocalError:
        return 'Error'


def writingCommand():
    try:
        sentences = Listen()
        sentence = ToEnglish(sentences)
        print(f">> You : {sentences}")
        return sentence
    except UnboundLocalError:
        return 'Error'


