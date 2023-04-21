import pyttsx3


def Speak(audio):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 140)
    engine.say(audio)
    print(f">> Jarvis : {audio}")
    print("_______________________________________________________")
    engine.runAndWait()

