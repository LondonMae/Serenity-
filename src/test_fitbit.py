import gather_keys_oauth2 as Oauth2
import fitbit
import datetime
from datetime import date
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from os.path import exists
import ast

# You will need to put in your own CLIENT_ID and CLIENT_SECRET as the ones below are fake
CLIENT_ID='238T5P'
CLIENT_SECRET='1d37c3db41c1eb5b84b770fb97069f59'

class TokenExpiredError(Exception):
    """Exception raised for expired access token (must sign in).
    """

    def __init__(self, message="Fitbit Access token expired"):
        super().__init__(message)

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = str(time_str).split(':')
    return int(h) * 3600 + int(m)

def get_day_diff(start, end):
    print(start)
    print(end)
    y1, m1, d1 = str(start).split('-')
    y2, m2, d2 = str(end).split('-')

    if (int(d1) == int(d2)):
        return 24*3600
    return 0

def today(day):
    date_list = str(day).split("-")
    return int(date_list[0]), int(date_list[1]), int(date_list[2])

def get_sleep_data(auth2_client, startTime, endTime):


    date_list = []
    df_list = []
    allDates = pd.date_range(start=endTime, end=startTime)

    def cleanup(break_date, date_list):
        # send data to csv for processing
        stages_df = pd.DataFrame(date_list)
        if exists("sleep3.csv"):
            if len(date_list) != 0:
                with open('sleepDate3.txt', 'w') as f:
                    f.write(str(break_date))
                stages_df.to_csv('sleep3.csv', mode="a", index=False, header = "False")
        else:
            if len(date_list) != 0:
                with open('sleepDate3.txt', 'w') as f:
                    f.write(str(break_date))
                stages_df.to_csv('sleep3.csv', mode="w", index=False, header = "True")

    break_date = next_date
    for oneDate in allDates:

        # get request from Fitbit
        oneDate = oneDate.date().strftime("%Y-%m-%d")
        break_date = oneDate
        print(break_date)
        try:
            oneDayData = dict(auth2_client.sleep(date=oneDate))

            #only save if we have good data
            if len(oneDayData["sleep"]) > 0 and oneDayData["sleep"][0]["isMainSleep"] and "stages" in oneDayData["summary"] and oneDayData["summary"]["stages"]["deep"] != 0:

                data = dict()

                # format times
                endDate, endtime = oneDayData["sleep"][0]["endTime"].split("T")
                startDate, starttime = oneDayData["sleep"][0]["startTime"].split("T")
                endtime = get_sec(endtime)
                starttime = get_sec(starttime)
                startinc = get_day_diff(startDate, endDate)
                starttime+=startinc

                # put data to dict
                data["endTime"] = endtime
                data["startTime"] = starttime
                data["minutesAsleep"] = oneDayData["sleep"][0]["minutesAsleep"]
                data["minutesAwake"] = oneDayData["sleep"][0]["minutesAwake"]
                data["deep"] = oneDayData["summary"]["stages"]["deep"]
                data["rem"] = oneDayData["summary"]["stages"]["rem"]
                date_list.append(data)
        except fitbit.exceptions.HTTPTooManyRequests as e:  # This is the correct syntax
                break

    cleanup(break_date, date_list)


try:
    f = open('fitbit_data.txt', 'r')
    token_dict = ast.literal_eval(f.readline())
    f.close()
    print(token_dict["expires_at"])
    expires_at = float(token_dict["expires_at"])
    if (expires_at < time.time()):
        raise TokenExpiredError()
    ACCESS_TOKEN = str(token_dict["accessToken"])
    print("token :" + ACCESS_TOKEN)
    REFRESH_TOKEN = str(token_dict["refreshToken"])
except TokenExpiredError:
    print("token is expired. Please log in again in your web browser")
except FileNotFoundError:
    print("cannot access fitbit data. Have you logged in in your browser?")
else:
    # requesting access from user
    auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN, )
    # This is the date of data that I want.
    dayTS = date.today()
    year, month, day = today(dayTS)
    startTime = datetime.datetime(year = year, month = month, day = day)

    dt = datetime.datetime(year=year, month=month, day=day)
    next_chunk = dt.timestamp() - 150*24*60*60
    next_date = datetime.datetime.fromtimestamp(next_chunk).strftime("%Y-%m-%d")
    if exists("sleepDate3.txt"):
        f = open('sleepDate3.txt', 'r')
        next_date = f.readline()
        f.close()
    year, month, day = today(next_date)
    endTime = datetime.datetime(year = year, month = month, day = day)
    print(startTime, endTime)
    get_sleep_data(auth2_client, startTime, endTime)
