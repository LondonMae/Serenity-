# This Python script plays a song
# recommended for a user that has
# high energy and high valence

import requests
import json
import random
import spotipy
import webbrowser
import json
import time

# get auth token
with open('user_data/test.txt') as f:
    token_dict = json.load(f)
token = token_dict['access_token']

# connect to user's spotify account
sp = spotipy.Spotify(auth=token)
user = sp.current_user()

# given a song and a player, start music
def play(uri, web_player):
    sp.start_playback(uris=[uri], device_id = web_player)

# returen specific track
def get_track(tracks, i, type="items"):
    return tracks[type][i]

# return track feature
def get_track_feature(song, feature="name"):
    return song[feature]

headers = {
    "Authorization": "Bearer " + token
}
#DEBUG
print(headers)

limit=50 # AMOUNT OF soungs we are pulling
recently_played_link = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=" + str(limit) #gets users recent top tracks

# make API request
res = requests.get(recently_played_link, headers = headers)
parsed = json.loads(res.text)

# pick 5 random songs from user's top 50
uris = []
for i in range(5):
    rand = random.randint(0, 49)
    song = get_track(parsed, rand)
    uri = get_track_feature(song, feature="uri")
    uris.append(uri)

# Generate recommendations given song picks
recommendations_link = "https://api.spotify.com/v1/recommendations?limit=1&seed_tracks="
for i in range(len(uris)):
    recommendations_link+=uris[i].partition(":")[2].partition(":")[2]
    if (i<len(uris)-1):
        recommendations_link+="%2C"
recommendations_link += "&min_energy=.6&max_energy=1&min_valence=.6&max_valence=1" # songs with high energy

res = requests.get(recommendations_link, headers = headers) # API request
parsed = json.loads(res.text)

# this is the song we will play
song = get_track(parsed, 0, type="tracks")
uri = get_track_feature(song, feature="uri")

# active devices
res = sp.devices()
res = res["devices"]

# first player
web_player = res[0]["id"]
print("first", web_player) # DEBUG
web_name = res[i]["name"] # debug

for i in range(len(res)):
    print (res[i]["name"]) # debug
    print(res[i]["id"])

device_id = "test"
# next phase: how can we dynamically get this ID
def alarm():
    play(uri,device_id)
