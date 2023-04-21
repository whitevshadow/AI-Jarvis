import os
from time import sleep

from Body.Speaker import Speak


def Call(number):
    sleep(1)
    os.system(f'adb shell am start -a android.intent.action.CALL -d tel:+91' + number)
    sleep(3)
    os.system('adb shell input tap 900 1050')


def Ans_Call():
    os.system('adb shell input keyevent 5')
    sleep(2)
    os.system('adb shell input tap 900 1050')


def End_Call():
    os.system('adb shell input tap 530 2130')


def Unlock():
    os.system('adb shell input keyevent 82')
    sleep(0.5)
    os.system('adb shell input keyevent 82')
    sleep(0.5)
    os.system('adb shell input keyevent 7')
    os.system('adb shell input keyevent 8')
    os.system('adb shell input keyevent 7')
    os.system('adb shell input keyevent 14')


Contact = {
    "harshal": "9172691064",
    "ajay": "9823513202",
    "athrav": "9021144118",
    "my": "9604304414"
}


def Call_number(sentences):
    contact_name = str(sentences).lower()
    names = list(Contact.keys())
    for person in names:
        try:
            if person in contact_name:
                num = f"{Contact[person]}"
                Speak(f"Sir! Calling {person}")
                Call(num)
                break
        except:
            Speak("Sir! There is No Number For the Given Name to make voice call")

