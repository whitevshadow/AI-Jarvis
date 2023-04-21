import datetime

import pywhatkit
from Body.Microphone import writingCommand
from Body.Speaker import Speak


def Whatsapp_msg(number, name):
    Speak(f"Sir ! Tell me what message you want to send to {name}")
    Message = writingCommand()
    time = datetime.datetime.now()
    hr = time.hour
    minute = time.minute
    minute = minute + 1
    pywhatkit.sendwhatmsg(f"+91{number}", Message, hr, minute)

