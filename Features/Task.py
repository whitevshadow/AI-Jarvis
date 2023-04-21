from time import sleep
import pyautogui
import pywhatkit as pywhatkit
import requests
from Body.Speaker import Speak
from Features.OS.Current_dur import Curr_time, Curr_date, Curr_day
from Features.OS.Notepad import create_note
from Features.OS.Speedtest import Speed_test
from Features.OS.Volume_control import change_volume
from Features.OS.Windows import Shutdown_pc, Lock_pc, battery_per, Screen_shot
from Features.Phone.Activity import Call_number, Ans_Call, End_Call, Unlock
from Features.Phone.find_phone import find_phone
from Features.Social_media.Instagram import profile_info
from Features.Social_media.Whatsapp import Whatsapp_msg
from Features.Web_Scraping.IP_address import Ip_address
from Features.Web_Scraping.Location import My_Location
from Features.Web_Scraping.News import latest_news
from Features.Web_Scraping.Thoughts import thought_day
from Features.Web_Scraping.Weather import get_Weather

Contact = {
    "harshal": "9172691064",
    "ajay": "9823513202",
    "goku": "9021144118",
    "my": "9604304414"
}


def random_stuff(sentences):
    url = "https://random-stuff-api.p.rapidapi.com/ai/response"

    text = sentences

    querystring = {"message": f"{text}", "bot_name": "Jarvis", "bot_gender": "male ",
                   "bot_master": "White_Shadows", "bot_age": "18", "bot_company": "MIT WPU",
                   "bot_location": "India (OPTIONAL)", "bot_email": "anishbochare@gmail.com",
                   "bot_build": "Public (OPTIONAL)", "bot_birth_year": "2021", "bot_birth_date": "3 March 2021",
                   "bot_birth_place": "India (OPTIONAL)", "bot_favorite_color": "Red",
                   "bot_favorite_book": "Tony Stark",
                   "bot_favorite_band": "Imagine Doggos (OPTIONAL)", "bot_favorite_artist": "Eminem (OPTIONAL)",
                   "bot_favorite_actress": "Emma Watson (OPTIONAL)", "bot_favorite_actor": "Jim Carrey (OPTIONAL)",
                   "user_id": "420"}

    headers = {
        "Authorization": "HCjo5Y4B4RDD",
        "X-RapidAPI-Key": "0477f85d5cmsh94bbbb1f4cc64a5p109fbbjsncdd6553ee50c",
        "X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    r = response.text
    r = r.split('"message":"')
    r = r[1]
    r = r.replace('"}', "").replace('"', '').replace('warning', '').replace(':No', '').replace(',', '')

    Speak(r)


def Functions(tag, sentences=""):
    try:
        if 'Exit' in tag:
            Speak("Good Bye, Sir. have a Nice Day :)")
            exit()

        elif 'Cur_Time' in tag:
            Time = Curr_time()
            Speak(Time)

        elif "Today_date" in tag:
            Date = Curr_date()
            Speak(Date)

        elif "Today_day" in tag:
            Day = Curr_day()
            Speak(Day)

        elif "Notepad" in tag:
            Speak("Okay, I am Ready to Write a Note")
            create_note()

        elif "Speedtest" in tag:
            Speed_Result = Speed_test()
            Speak(Speed_Result)

        elif "increase_vol" in tag:
            Volume = change_volume(2)
            Speak(Volume)

        elif "decrease_vol" in tag:
            Volume = change_volume(-2)
            Speak(Volume)

        elif "Shutdown_Device" in tag:
            Shut_status = Shutdown_pc()
            Speak(Shut_status)

        elif "Lock" in tag:
            Lock_status = Lock_pc()
            Speak(Lock_status)

        elif "Battery_Per" in tag:
            Percentage = battery_per()
            Speak(Percentage)

        elif "Screen_shot" in tag:
            Screenshot = Screen_shot()
            Speak(Screenshot)

        elif "My_PC_IP" in tag:
            ip_address = Ip_address()
            Speak(ip_address)

        elif "My_Location" in tag:
            address = My_Location()
            Speak(address)

        elif "News" in tag:
            News = latest_news()
            Speak(News)

        elif "Weather" in tag:
            get_Weather(sentences)

        elif "Music" in tag:
            song = str(sentences).replace("play", "").replace("music", "").replace("youtube", "")
            Speak("Sir! Playing the Song on YouTube")
            pywhatkit.playonyt(song)
            sleep(3)
            pyautogui.press('f')

        elif "Thoughts" in tag:
            thought = thought_day()
            Speak(thought)

        elif "Whatsapp_msg" in tag:
            contact_name = str(sentences).lower()
            names = list(Contact.keys())
            for person in names:
                try:
                    if person in contact_name:
                        num = f"{Contact[person]}"
                        Whatsapp_msg(num, person)

                        break
                except:
                    Speak("Sir! There is No Number For the Given Name to send Message")

        elif "Insta_Profile" in tag:
            profile_info(sentences)

        elif "Phone_Call" in tag:
            Call_number(sentences)

        elif "Ans_call" in tag:
            Speak("Sir! I am Picking up the Phone call.")
            Ans_Call()

        elif "End_Call" in tag:
            Speak("Sir! I am Ending the Phone call.")
            End_Call()

        elif "Phone_Unlock" in tag:
            Unlock()
            Speak("Sir! Your Phone has been Unlocked.")

        elif "Self_Call" in tag:
            Speak("Sir ! I am Calling on Your Phone")
            find_phone()

        else:
            random_stuff(sentences)

    except Exception as e:
        print(e)




