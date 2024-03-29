from phue import Bridge
import pandas as pd
import time
from datetime import datetime, date

bridge_ip = 'secret/hue_ip.txt' # secret
b = Bridge(bridge_ip) # connect to hue bridge using IP address
b.connect()  # run first time to establish connection

date = date.today()
now = datetime.now()

def get_light_status():
    
    # getting state of light
    light_on = b.get_light(4, 'on')
    light_colormode = b.get_light(4, 'colormode')
    light_bri = b.get_light(4, 'bri')
    light_hue = b.get_light(4, 'hue')
    light_sat = b.get_light(4, 'sat')
    light_xy = b.get_light(4, 'xy')
    light_ct = b.get_light(4, 'ct')
    
    date_ = date.today()
    now = datetime.now()

    current_date = date_.strftime("%d/%m/%y")
    current_time = now.strftime("%H:%M")
    
    return current_date, current_time, light_on, light_colormode, light_bri, light_hue, light_sat, light_xy, light_ct


# create dataframe to hold the data
df = pd.DataFrame(columns=["date", "time", "light_on", "light_colormode", "light_bri", "light_hue", "light_sat", "light_xy", "light_ct"])


def call_hue(df):
  current_date, current_time, light_on, light_colormode, light_bri, light_hue, light_sat, light_xy, light_ct = get_light_status()

  df = df.append({"date":current_date, "time": current_time, "light_on":light_on, "light_colormode":light_colormode, "light_bri":light_bri, "light_hue":light_hue, "light_sat":light_sat, "light_xy":light_xy, "light_ct":light_ct}, ignore_index=True)

  print(df)
  return df

while True:
    time.sleep(90) # run every 90s
    df = call_hue(df)
  
df.to_csv('hue_data.csv') # convert dataframe into csv file