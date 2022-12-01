import time
import schedule
import threading
import sys
import music
import lights
# import sleep_alg
import datetime

# ideally get from interface
hour = sys.argv[1]
if (len(hour) == 1):
    hour = "0" + hour
minute = sys.argv[2]

wake_time = hour + ":" + minute

print(wake_time)

# for completion checking
music_complete = False
lights_complete = False
nav_complete = False
data_complete = False

def play_music():
    print("music")
    global music_complete
    music_complete = True
    music.alarm()

def turn_on_lights():
    print("lights")
    global lights_complete
    lights_complete = True
    #lights.sunrise()

def nav():
    print("nav")
    global nav_complete
    nav_complete = True

def display_data():
    print("data")
    td = time.strptime(wake_time,'%H:%M')
    td = datetime.timedelta(hours=td.tm_hour,minutes=td.tm_min,seconds=td.tm_sec).total_seconds()/3600
    # sleep_alg.predict(td)
    global data_complete
    data_complete = True

def execute_once(f):
    job_thread = threading.Thread(target = f)
    job_thread.start()
    print("done")
    # Do some work that only needs to happen once...
    return schedule.CancelJob

schedule.every().day.at(wake_time).do(execute_once, nav)
schedule.every().day.at(wake_time).do(execute_once, play_music)
schedule.every().day.at(wake_time).do(execute_once, turn_on_lights)
schedule.every().day.at(wake_time).do(execute_once, display_data)

while True:
    print (music_complete and nav_complete and lights_complete and data_complete)
    if music_complete and nav_complete and lights_complete and data_complete:
        break
    schedule.run_pending()
    time.sleep(1)
