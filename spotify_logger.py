import requests
import spotipy
import requests
import pandas as pd
import ast
import json
from typing import List
from os import listdir
import spotipy.util as util

username = '1168538196' # spotify account username
client_id ='b6086497a7d0436da80bbfda6753b36d' # developer details
client_secret = 'secret/client_secret.txt' # secret
redirect_uri = 'http://localhost:1410/'
scope = 'user-read-recently-played' # permissions required for access

token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri) # generate token

spotify = spotipy.Spotify(auth=token) # use token for authorisation


def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played?after=1638816492', limit=limit) # get recent listening history

def spotify_json_clean(data, df, i):
    played_at = data["items"][i]["played_at"]
    track_id = data["items"][i]["track"]["id"]
    
    played_at_date = played_at[8:10] + '/' + played_at[5:7] + '/' + played_at[0:4]
    played_at_time = played_at[11:13] + ':' + played_at[14:16]
    
    df = df.append({"played_at_date":played_at_date, "played_at_time":played_at_time, "track_id":track_id}, ignore_index=True) # add data to dataframe
    
    return df


data_= spotify.current_user_recently_played(limit=50)

out_file = open("data_.json","w") # data is returned as a json file
out_file.write(json.dumps(data_, sort_keys=True, indent=2)) # encode data
out_file.close()

with open('data_.json') as json_file:
    data = json.load(json_file) # load now encoded data

df = pd.DataFrame(columns=["played_at_date", "played_at_time", "track_id"]) # establish dataframe
    
for i in range(50):
    df = spotify_json_clean(data, df, i) # get values for all 50 tracks in json
    

df.to_csv('spotify_data.csv') # create csv