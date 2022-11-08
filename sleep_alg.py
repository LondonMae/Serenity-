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
