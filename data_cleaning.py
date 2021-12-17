import pandas as pd
import spotipy
import spotipy.util as util


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

def get_song_features(track_id):
    features = sp.audio_features(tracks=track_id)
    track_features = features[0] 
    
    # store the track audio features for later use
    acousticness = track_features['acousticness']
    danceability = track_features['danceability']
    energy = track_features['energy']
    valence = track_features['valence']
    
    return acousticness, danceability, energy, valence

# read and convert all csvs into lists for easy manipulation
df_sensors = pd.read_csv('sensor_data.csv')
df_spotify = pd.read_csv('spotify_data.csv')
df_hue = pd.read_csv('hue_data.csv')

df_sensors = df_sensors.values.tolist()
df_spotify = df_spotify.values.tolist()
df_hue = df_hue.values.tolist()

combined = []

for song in df_spotify:
    
    for row in df_sensors:
    
        if song[1] == row[1] and song[2] == row[2]: # if date and time is same
            
            for val in df_hue:
                
                #splitting up time data for easier analysis
                hue_hour = int(val[2][:2])
                hue_min = int(val[2][3:5])
                
                song_hour = int(song[2][:2])
                song_min = int(song[2][3:5])
                
                # accounting for how readings were taken every minute and a half - every third minute will not be logged, but a song may have started at that time
                if (val[1] == song[1] and val[2] == song[2] and val[3] == True) or (val[1] == song[1] and val[3] == True and hue_hour == song_hour and (hue_min+1) == song_min):

                    acousticness, danceability, energy, valence = get_song_features(song[3])
                    
                    # get all necessary features from each database list
                    to_append = [song[1], song[2], val[5], val[6], val[7], row[3], row[4], row[5], row[6], song[3], acousticness, danceability, energy, valence]
                    combined.append(to_append)
                    break


print(combined)

# create dataframe using data
df_ = pd.DataFrame (combined, columns =['date', 'time', 'light_bri', 'light_hue', 'light_sat', 'ldr', 'red', 'green', 'blue', 'song_id', 'acousticness', 'danceability', 'energy', 'valence'])
df_.to_csv('combined_data.csv') # export as csv