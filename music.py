import requests
import json
import random
import spotipy
import webbrowser

clientID = "2c4caf3e40664518b5f62dbd9cfc6e4f"
clientSecret = "42c33e9f97a24f8eae42741e9fad2237"
redirectURI = 'http://google.com/'
scope = "user-top-read,user-read-recently-played,user-read-playback-state,user-modify-playback-state"
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI, scope=scope)
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']
sp = spotipy.Spotify(auth=token)
user = sp.current_user()

def play(uri, web_player):
    # Change track
    sp.start_playback(uris=[uri], device_id = web_player)

def get_track(tracks, i, type="items"):
    return tracks[type][i]

def get_track_feature(song, feature="name"):
    return song[feature]

headers = {
    "Authorization": "Bearer " + token
}

print(headers)

limit=50
recently_played_link = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=" + str(limit)

res = requests.get(recently_played_link, headers = headers)

parsed = json.loads(res.text)

uris = []

for i in range(5):
    rand = random.randint(0, 49)
    song = get_track(parsed, rand)
    uri = get_track_feature(song, feature="uri")
    print (uri)
    uris.append(uri)

recommendations_link = "https://api.spotify.com/v1/recommendations?limit=1&seed_tracks="


for i in range(len(uris)):
    recommendations_link+=uris[i].partition(":")[2].partition(":")[2]
    if (i<len(uris)-1):
        recommendations_link+="%2C"

recommendations_link += "&min_energy=.6&max_energy=1&min_valence=.6&max_valence=1"

print(recommendations_link)

res = requests.get(recommendations_link, headers = headers)

print(res.text)
parsed = json.loads(res.text)

print(parsed)

song = get_track(parsed, 0, type="tracks")
uri = get_track_feature(song, feature="uri")

res = sp.devices()
res = res["devices"]

print(res)

web_player = res[0]["id"]

for i in range(len(res)):
    print (res[i]["name"])
    if res[i]["name"] == "Dubolt Web Player":
        print("hi")
        web_player= res[i]["id"]
print(web_player)

play(uri, web_player)
