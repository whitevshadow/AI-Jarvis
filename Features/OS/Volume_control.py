import pyautogui


def change_volume(change):
    # Press the volume up/down key a certain number of times
    if change > 0:
        for i in range(int(change * 10)):
            pyautogui.press("volumeup")
            return "Volume has been Increased"
    elif change < 0:
        for i in range(int(-change * 10)):
            pyautogui.press("volumedown")
            return "Volume has been Decreased"
