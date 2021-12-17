import requests
import spotipy
import requests
import pandas as pd
import ast
import json
from typing import List
from os import listdir
import spotipy.util as util

username = '1168538196'
client_id ='b6086497a7d0436da80bbfda6753b36d'
client_secret = 'secret/client_secret.txt' # secret
redirect_uri = 'http://localhost:1410/'
scope = 'user-read-recently-played'

token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)

spotify = spotipy.Spotify(auth=token)


def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played?after=1638816492', limit=limit)

def spotify_json_clean(data, df, i):
    played_at = data["items"][i]["played_at"]
    track_id = data["items"][i]["track"]["id"]
    duration_ms = data["items"][i]["track"]["duration_ms"]
    track_uri = data["items"][i]["track"]["uri"]
    
    played_at_date = played_at[8:10] + '/' + played_at[5:7] + '/' + played_at[0:4]
    played_at_time = played_at[11:13] + ':' + played_at[14:16]
    
    df = df.append({"played_at_date":played_at_date, "played_at_time":played_at_time, "track_id":track_id, "track_uri":track_uri, "duration_ms":duration_ms}, ignore_index=True)
    
    return df


data_= spotify.current_user_recently_played(limit=50)

out_file = open("data_.json","w") 
out_file.write(json.dumps(data_, sort_keys=True, indent=2)) 
out_file.close()

print(json.dumps(data_, sort_keys=True, indent=2))

with open('data_.json') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(columns=["played_at_date", "played_at_time", "track_id", "track_uri", "duration_ms"])
    
for i in range(50):
    df = spotify_json_clean(data, df, i)
    

df.to_csv('spotify_data.csv')