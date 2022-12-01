# this script trains data and predicts a point
# based on various sleep factors pulled from fitbit


# example:
#
# these are the attributes that we will use:
# wakeup time, time in bed, minutes asleep, minutes awake, deep sleep

# - for the test point we will
#     - use alarm setting as wakeup time
#     - use time in bed as a sliding option (where we recommend and let the user modify to see changing sleep score)
#     - for minutes asleep and awake and asleep we will take the average or median (method of average)
#     - deep sleep is what we are predicting

# maximize deep sleep but don't let sleep last longer than 10 hours

from collections import Counter
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import sys
import requests

def knn(data, query, k, distance_fn, choice_fn):
    neighbor_distances_and_indices = []

    # 3. For each example in the data
    for index, example in enumerate(data):
        # 3.1 Calculate the distance between the query example and the current
        # example from the data.
        distance = distance_fn(example[:-1], query)

        # 3.2 Add the distance and the index of the example to an ordered collection
        neighbor_distances_and_indices.append((distance, index))

    # 4. Sort the ordered collection of distances and indices from
    # smallest to largest (in ascending order) by the distances
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)

    # 5. Pick the first K entries from the sorted collection
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]

    # 6. Get the labels of the selected K entries
    k_nearest_labels = [data[i][-1] for distance, i in k_nearest_distances_and_indices]

    # 7. If regression (choice_fn = mean), return the average of the K labels
    # 8. If classification (choice_fn = mode), return the mode of the K labels
    return k_nearest_distances_and_indices , choice_fn(k_nearest_labels)

def mean(labels):
    return sum(labels) / len(labels)

def mode(labels):
    return Counter(labels).most_common(1)[0][0]

def euclidean_distance(point1, point2):
    sum_squared_distance = 0
    for i in range(len(point1)):
        sum_squared_distance += math.pow(point1[i] - point2[i], 2)
    return math.sqrt(sum_squared_distance)

def predict(h, m):
    if (len(h) == 1):
        h = "0" + hour
    wake_time = h + ":" + m
    td = time.strptime(wake_time,'%H:%M')
    alarm_time = datetime.timedelta(hours=td.tm_hour,minutes=td.tm_min,seconds=td.tm_sec).total_seconds()/3600

    stages_df = pd.read_csv("sleep.csv") # gets data

    # store all data as arrays
    deep = stages_df["deep"]
    rem = stages_df["rem"]
    awake = stages_df["minutesAwake"]
    asleep = stages_df["minutesAsleep"]
    sleep_time = stages_df["startTime"]
    awake_time = stages_df["endTime"]

    # compute averages
    avg = {"efficiency": 0, "deep percent": 0, "rem percent": 0, "Deep": 0, "Rem": 0, "Sleep": 0, "Start":0, "End":0, "Awake":0}
    for i in range(len(asleep)):
        avg["deep percent"] += (deep[i]/asleep[i])
        avg["rem percent"] += (rem[i]/asleep[i])
        avg["efficiency"] += (asleep[i]/(asleep[i] + awake[i]))
        avg["Deep"] += deep[i]
        avg["Rem"] += rem[i]
        avg["Sleep"] += asleep[i]/60
        avg["Awake"] += awake[i]/60
        avg["Start"] += sleep_time[i]/3600
        avg["End"] += awake_time[i]/3600

    # for displaying to user
    final_string = ""
    for type in avg:
        avg[type] /= len(asleep)
        final_string += "Average " + type + ": " + str(avg[type]) + "\n"


    # keep data foe prediction
    stages_df.pop("startTime")
    stages_df.pop("deep")
    stages_df.pop("minutesAwake")
    stages_df["endTime"] /= 3600
    reg_data = stages_df.values.tolist()

    # swap because we are predicting sleep given REM
    for i in range(len(reg_data)):
        temp = reg_data[i][1]
        reg_data[i][1] = reg_data[i][2]
        reg_data[i][2] = temp

    # run at 8 hours (60*8 = 480 minutes). if 0, keep increasing until we find 1
    # else, decrease until we find 0.

    # find first predicted 90 minutes, then recommend
    # this time + avg min to fall asleep rounded to nearest 15 minutes

    # ideally get this from interface
    #alarm_time = 6
    # optimal amount of REM
    test_rem = 90

    # Question:
    # given alarm time and ideal rem, when should they go to sleep?
    reg_query = [alarm_time, 90]
    reg_k_nearest_neighbors, reg_prediction = knn(
        reg_data, reg_query, k=4, distance_fn=euclidean_distance, choice_fn=mean
    )

    predicted_sleep = (alarm_time*60 - (reg_prediction+avg["Awake"]*60)) % (24*60)

    # write prediction to file
    final_string = "we predict that you should go to sleep at: " + str(time.strftime("%H:%M", time.gmtime(predicted_sleep*60)))
    data = {"prediction":final_string}

    print (final_string)
    with open('predictions.txt', 'w') as f:
        f.write(final_string)

hour = sys.argv[1]
minute = sys.argv[2]
predict(hour, minute)
