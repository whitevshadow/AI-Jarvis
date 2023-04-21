import os
import random
import threading
import tkinter
import sys
from tkinter.constants import BOTH, YES, NW
from Body.Microphone import MicExecution
from Brain.Face_trainer import Face_training
from Brain.Trainer import TasksExecutor, TrainTasks
from Features.Task import Functions
from Brain.Init import init


def jarvis():
    init()
    while True:
        sentences = MicExecution()
        word = TasksExecutor(sentences)
        Functions(word, sentences)


def Color_change():
    color = ['red', 'blue', 'white', 'gold', 'yellow']
    actual_color = random.choice(color)
    label.configure(foreground=actual_color)
    label.after(1000, Color_change)


def run():
    threading.Thread(target=jarvis).start()

    def flush(self):
        pass


def stop():
    os.system("TASKKILL /F /im python.exe") and os.system("TASKKILL /F /im Jarvis.py") and os.system(
        "TASKKILL /F /im Jarvis.exe")


def face_train():
    threading.Thread(target=Face_training).start()


def model_train():
    threading.Thread(target=TrainTasks).start()


screen_main = tkinter.Tk()
screen_main.title('Jarvis')
screen_main.configure(background='black', highlightbackground='blue', highlightthickness=5)
screen_main.attributes('-fullscreen', True)
screen_main.iconbitmap('GUI\\Icon\\jarvis.ico')

canvas = tkinter.Canvas(width=200, height=200, bg='black', highlightbackground='cyan', highlightthickness=5)
canvas.pack(expand=YES, fill=BOTH)
photo = tkinter.PhotoImage(file='GUI\\bg_jarvis.gif')
canvas.create_image(1010, 0, image=photo, anchor=NW)

start_button = tkinter.Button(screen_main, background='black', fg='red', font=('IRON MAN OF WAR 2 NCV', 40),
                              text='Start',
                              command=run)
start_button.place(x=1350, y=600)
stop_button = tkinter.Button(screen_main, background='black', fg='red', font=('IRON MAN OF WAR 2 NCV', 40), text='Stop',
                             command=stop)
stop_button.place(x=1600, y=600)

face_Train = tkinter.Button(screen_main, background='black', fg='red', font=('IRON MAN OF WAR 2 NCV', 40),
                            text='Face Train',
                            command=face_train)
face_Train.place(x=1050, y=750)

train = tkinter.Button(screen_main, background='black', fg='red', font=('IRON MAN OF WAR 2 NCV', 40),
                       text='Model Train',
                       command=model_train)
train.place(x=1300, y=750)

label = tkinter.Label(screen_main, font=('IRON MAN OF WAR 2 NCV', 70), text="JARVIS", background='black')
Color_change()
label.place(x=1480, y=900)

Color_change()

terminal = tkinter.Text(screen_main)
terminal.configure(background='black', fg='white', highlightbackground='red', highlightthickness=5)

terminal.configure(width=45, height=41.499)
terminal.configure(font=('Bruce Forever', 15))
terminal.place(x=13.5, y=13.48)


class Redirect:
    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see('end')


old_stdout = sys.stdout
sys.stdout = Redirect(terminal)
screen_main.mainloop()
