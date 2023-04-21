import datetime


def Curr_time():
    try:
        cur_time = datetime.datetime.now().strftime("%I:%M %p")
        data = f"Sir, The Current Time is {cur_time}"
        return data
    except:
        data_error = "There was a problem to Retrieve Time"
        return data_error


def Curr_date():
    try:
        cur_date = datetime.datetime.now().strftime("%d %B %Y")
        data = f"Sir, Today's Date is {cur_date}"
        return data
    except:
        data_error = "There was a problem to Retrieve Date"
        return data_error


def Curr_day():
    day = datetime.datetime.now().strftime("%A")
    data = f"Sir, Today's Day is {day}"
    return data
