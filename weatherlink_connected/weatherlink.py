# WeatherLink is a sensor that detects particulate matter in the air
# see https://www.davisinstruments.com

# It is very useful for determining the air quality in your home or office
# The tutorial (https://weatherlink.github.io/v2-api/tutorial) is very good but insufficient
# The code I found online was mostly incomplete, to say the least

import numpy as  np
import pandas as pd
import datetime
import time
import tzlocal
import matplotlib.pyplot as plt

import hashlib
import hmac
import time
from datetime import datetime
import urllib
import urllib.request
import json
from IPython.display import display

APIKeyv2 = 'p8gfl0ndkve9ydlpi9elxq3hkwkszt1a'
APISecret = 'fhrwrkawzyonkd3ppubd1zpjrkypsw24'


## ----------------------
## Read the stations data
## ----------------------

t               = int(time.time())
message_to_hash = "api-key{}t{}"\
                  .format(APIKeyv2, t)

apiSignature = hmac.new(
  APISecret.encode('utf-8'),
  message_to_hash.encode('utf-8'),
  hashlib.sha256
).hexdigest()

stations_url = "https://api.weatherlink.com/v2/stations?api-key={}&t={}&api-signature={}"\
               .format(APIKeyv2, t, apiSignature)
#print(stations_url,'\n')

with urllib.request.urlopen(stations_url) as url:
    data = json.loads(url.read().decode())
    #print(json.dumps(data, indent=4, sort_keys=False))

# in my case, there is only one station
# modifications are required if more than one
station_id   = data['stations'][0]['station_id']
#station_name = data['stations'][0]['station_name']
#print("\nstation_id:   {}\nstation_name: {}".format(station_id,station_name))

#print(type(data['stations']))
#print(type(data['generated_at']))
#print(" ")

for stations in data['stations']:
    #print(json.dumps(stations['station_name'], indent=4))
    Station_str = stations['station_name']
    #print(Station_str)

UTC_timesamp = data['generated_at']
#print(UTC_timesamp)
dt = datetime.fromtimestamp(data['generated_at'])
#print(dt)

#print(Station_str + ' contacted at ' + str(dt))
#print()

## --------------------------------
## Read the current conditions data
## --------------------------------

t = int(time.time())
message_to_hash = "api-key{}station-id{}t{}".format(APIKeyv2, station_id, t)
#print(message_to_hash)

apiSignature = hmac.new(
  APISecret.encode('utf-8'),
  message_to_hash.encode('utf-8'),
  hashlib.sha256
).hexdigest()

current_url = "https://api.weatherlink.com/v2/current/{}?api-key={}&t={}&api-signature={}"\
              .format(station_id, APIKeyv2, t, apiSignature)
#print(current_url,'\n')

with urllib.request.urlopen(current_url) as url:
    data_values = json.loads(url.read().decode())
    #print(json.dumps(data_values, indent=4, sort_keys=True))

#print(json.dumps(data_values['sensors'][1]['data'][0]['hum'], indent = 4))

humidity = data_values['sensors'][1]['data'][0]['hum']

print(Station_str + ' contacted at ' + str(dt) + ' with humidity reported to be at ' + str(humidity))
#for values in data_values['sensors'][1]['data']:
#print(values)

#print(json.dumps(data_values['sensors'][1]['data'], indent=4))

#outside_temp = data_values['sensors'][0]['data'][1]['temp']
#print(outside_temp)

# current_data  = data['sensors'][0]['data'][0]
# current_items = ["hum_in","temp_in"]

# item_data = {}
# for item in current_items:
#     item_data[item] = int(current_data[item])

# pd.DataFrame(data=item_data,index=[pd.Timestamp(datetime.datetime.today())])

## --------------------
## Read historical data
## --------------------

#end_timestamp   = int(time.time())
#start_timestamp = end_timestamp - 86400 # maximum: 24 hours

#t               = int(time.time())
#message_to_hash = "api-key{}end-timestamp{}start-timestamp{}station-id{}t{}"\
#                  .format(APIKeyv2, end_timestamp, start_timestamp, station_id, t)
#print(message_to_hash)

#apiSignature = hmac.new(
#  APISecret.encode('utf-8'),
#  message_to_hash.encode('utf-8'),
#  hashlib.sha256
#).hexdigest()
#print(apiSignature)

# historic_url = "https://api.weatherlink.com/v2/historic/{}?api-key={}&t={}&start-timestamp={}&end-timestamp={}&api-signature={}"\
#                .format(station_id, APIKeyv2, t, start_timestamp, end_timestamp, apiSignature)
# #print(historic_url,'\n')

# with urllib.request.urlopen(historic_url) as url:
#     data = json.loads(url.read().decode())


# df         = pd.DataFrame(data=data['sensors'][0]['data'])

# local_timezone = tzlocal.get_localzone()

# df['date'] = [pd.Timestamp(datetime.datetime.fromtimestamp(ts, local_timezone).strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)")) for ts in df.ts]
# df.set_index('date',inplace=True)
# df.sort_index(inplace=True)
# display(df)

# ## Plot 24 hours of particulate matter

# df.loc[:, ['hum_in_hi', 'dew_point_in']].plot(figsize=(20, 20))
# plt.grid()
# plt.axhline(y=12) # PM2.5 max healthy level
# plt.show()