from time import sleep
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import struct
import pyaudio
import pvporcupine

from Body.Microphone import MicExecution
from Body.Speaker import Speak

email_id = 'riddhiarpan2211@gmail.com'
password = 'ridarp@2211'

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
#chrome_options.add_argument('--headless')
Path_ofDriver = 'Drivers\\chromedriver.exe'
s = Service('Drivers\\chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()


def login():
    Website = 'https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F'
    driver.get(Website)
    driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(email_id)
    driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="login-button"]/span[1]').click()
    sleep(5)
    try:
        driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button').click()
    except selenium.common.exceptions.ElementNotInteractableException:
        pass


def bumblelee():
    access_key = "RYHozjPJuklGvd/1+6i8aIc2Se48CoS0QdJLBI3CscGnY72CjRqZ7g=="
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["bumblebee"], access_key=access_key)
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,
                                 channels=1,
                                 format=pyaudio.paInt16,
                                 input=True,
                                 frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                Speak("Make Your Word, Master")
                break

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# //*[@id="main"]/div/div[2]/div[2]/footer/div/div[3]/div/button[2]


def music_mode():
    sleep(3)
    driver.find_element(By.XPATH,
                        '/html/body/div[4]/div/div[2]/div[2]/footer/div/div[3]/div/button').click()
    driver.find_element(By.XPATH,
                        '//*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/button[3]').click()


def play_song():
    driver.find_element(By.XPATH,
                        '//*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/button[3]').click()
    sec = time()
    sleep(sec)


# //*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/button[4]


def next_song():
    driver.find_element(By.XPATH,
                        '//*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/button[4]').click()


def pre_song():
    driver.find_element(By.XPATH,
                        '//*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/button[2]').click()


# //*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[1]


def like_song():
    driver.find_element(By.XPATH,
                        '/html/body/div[4]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/button').click()
    print("LIKED")


def time():
    song_time = driver.find_element(By.XPATH,
                                    '//*[@id="main"]/div/div[5]/div/div[2]/div[3]/div[2]/div/div[1]/div[3]').text
    minutes, seconds = song_time.split(":")
    total_seconds = int(minutes) * 60 + int(seconds)
    return total_seconds


def Bumblebee_mode():
    login()
    music_mode()
    while True:
        bumblelee()
        cmd = input("Enter : ")

        if "like" in cmd or "favourite" in cmd:
            like_song()

        elif "change" in cmd or "next" in cmd:
            next_song()

        elif "previous" in cmd or "back" in cmd:
            pre_song()

        elif "exit" in cmd or "good bye" in cmd or "bye" in cmd:
            break

        else:
            Speak("Can You Speak it again")

