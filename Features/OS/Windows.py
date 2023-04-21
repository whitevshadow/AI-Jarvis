import ctypes
import datetime
import subprocess
import psutil as psutil
import pyautogui
from plyer import notification


def Shutdown_pc():
    try:
        process_status = "Hold On a Sec ! Your system is on its way to shut down in 10 sec"

        return process_status
    except:
        process_error = "Sir !, I am Unable to Shutdown the Device"
        return process_error


def Lock_pc():
    try:
        process_status = "Locking the device"
        ctypes.windll.user32.LockWorkStation()
        return process_status
    except:
        process_error = "Sir !, I am Unable to Lock Your Device"
        return process_error


def battery_per():
    try:
        battery = psutil.sensors_battery()
        percent = battery.percent
        Laptop_per = f"Sir Laptop Battery is {percent} percent"
        return Laptop_per
    except StopIteration:
        Laptop_error = "You are on Computer without battery"
        return Laptop_error


def Screen_shot():
    screenshot = pyautogui.screenshot()

    img_name = datetime.datetime.now().strftime("%d_%B_%Y_%I_%M_%p")
    img = str(img_name)
    screenshot.save(f"{img}.png")
    return "Screenshot taken Successfully"


