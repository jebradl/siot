from phue import Bridge
import pandas as pd
import time
from datetime import datetime, date
import spotipy
import spotipy.util as util

bridge_ip = 'secret/hue_ip.txt' # secret
b = Bridge(bridge_ip) 
b.connect()

username = '1168538196'
client_id ='b6086497a7d0436da80bbfda6753b36d'
client_secret = 'secret/client_secret.txt' # secret
redirect_uri = 'http://localhost:1410/'
scope = 'user-read-recently-played user-read-playback-state'

token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)

current_song = sp.currently_playing()
features = sp.audio_features(tracks=[current_song["item"]["id"]])


def change_lights_w_music():
    current_song = sp.currently_playing()
    print("now playing:", current_song["item"]["name"], "•", current_song["item"]["artists"][0]["name"])
    
    features = sp.audio_features(tracks=[current_song["item"]["id"]])
    track_features = features[0]
    
    xy_1 = [float(track_features["energy"]), float(track_features["valence"])]
    xy_2 = [float(track_features["danceability"]), float(track_features["energy"])]
    xy_3 = [float(track_features["valence"]), float(track_features["acousticness"])]

    transition_1 = ((xy_1[0]-xy_2[0])**2 + (xy_1[1]-xy_2[1])**2)**0.5
    transition_2 = ((xy_3[0]-xy_2[0])**2 + (xy_3[1]-xy_2[1])**2)**0.5
    transition_3 = ((xy_1[0]-xy_3[0])**2 + (xy_1[1]-xy_3[1])**2)**0.5

    transitions = [transition_1, transition_2, transition_3]
    
    bpm = float(track_features["tempo"])
    beat_time = 60 / bpm
    
    if float(track_features["energy"])>0.5:
        transition_min = 8
    else:
        transition_min = 12
    
    while beat_time <= transition_min:
        beat_time *= 2
    
    transition_time = (beat_time*10)-30
    
    while True:
        for i in [xy_1, xy_2, xy_3]:
            b.set_light(4, 'xy', i, transitiontime=transition_time)
            for j in range(4):
                time.sleep(beat_time/4)
                song_update(current_song)


def song_update(current_song):
    check_song = sp.currently_playing()
    #print("♩♬♩")
    if current_song["item"]["id"] != check_song["item"]["id"]:
        print("song changing...")
        change_lights_w_music()
        
            
change_lights_w_music()
