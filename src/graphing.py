from collections import Counter
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import seaborn as sns
import sys
import requests

stages_df = pd.read_csv("sleep.csv") # gets data
plt.plot(stages_df["minutesAsleep"], stages_df["rem"], "ro")
plt.xlabel('REM')
plt.ylabel('Minutes Asleep')
plt.show()
