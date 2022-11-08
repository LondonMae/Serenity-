import time
import schedule
import threading
import sys

wake_time = "08:31"
music = False
lights = False
nav_complete = False

def play_music():
    print("music")
    global music
    music = True
    print (music)

def turn_on_lights():
    print("lights")
    global lights
    lights = True

def nav():
    print("nav")
    global nav_complete
    nav_complete = True

def execute_once(f):
    job_thread = threading.Thread(target = f)
    job_thread.start()
    print("done")
    # Do some work that only needs to happen once...
    return schedule.CancelJob

schedule.every().day.at(wake_time).do(execute_once, nav)
schedule.every().day.at(wake_time).do(execute_once, play_music)
schedule.every().day.at(wake_time).do(execute_once, turn_on_lights)

while True:
    if music and nav_complete and lights:
        break
    schedule.run_pending()
    time.sleep(1)
