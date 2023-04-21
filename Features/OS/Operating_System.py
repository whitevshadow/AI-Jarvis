from Body.Speaker import Speak
from Features.OS.Current_dur import Curr_time, Curr_date, Curr_day
from Features.OS.Notepad import create_note
from Features.OS.Speedtest import Speed_test
from Features.OS.Volume_control import change_volume
from Features.OS.Windows import Shutdown_pc, Lock_pc, battery_per, Screen_shot


def OS_task(tag):
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

    else:
        pass



