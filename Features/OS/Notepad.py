import datetime
import os
from Body.Microphone import Listen, ToEnglish, writingCommand
from Body.Speaker import Speak


def create_note():
    try:
        write = str(writingCommand())
        Speak(f"You Told me to Remember !!\n{write}")
        note_time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().date()
        name = f"{date} : {note_time}"
        filename = str(name).replace(":", "-") + ".txt"
        with open(filename, "w") as file:
            file.write(write)
        path_1 = "" + str(filename)
        path_2 = "Notepad\\" + str(filename)
        os.rename(path_1, path_2)
        os.startfile(path_2)
        os.system("TASKKILL /F /im Notepad.exe")
        Speak("Note has been Written")
    except:
        Speak("Note has been Written")


