import gather_keys_oauth2 as Oauth2
import fitbit
import datetime
import pandas as pd

# You will need to put in your own CLIENT_ID and CLIENT_SECRET as the ones below are fake
CLIENT_ID='238T5P'
CLIENT_SECRET='1d37c3db41c1eb5b84b770fb97069f59'

# collect user info from server
server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

# save authotrization token
with open('fitbit_data.txt', 'w') as f:
    f.write(str(server.fitbit.client.session.token))

# tokens
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
# requesting access from user
auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN, )





# This is the date of data that I want.
startTime = pd.datetime(year = 2022, month = 3, day = 1)
endTime = pd.datetime(year = 2022, month = 3, day = 1)



date_list = []
df_list = []
allDates = pd.date_range(start=startTime, end=endTime)

for oneDate in allDates:
    oneDate = oneDate.date().strftime("%Y-%m-%d")
    oneDayData = dict(auth2_client.sleep(date=oneDate))
    oneDayData.pop("minutesData", None)
    print(oneDayData["minutesData"])
    stages_df = pd.DataFrame(oneDayData["sleep"])

    print(stages_df)
