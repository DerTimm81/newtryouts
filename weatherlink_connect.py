import numpy as  np
import pandas as pd
import datetime
import tzlocal
import matplotlib.pyplot as plt


from configparser import ConfigParser
import time
import hashlib
import hmac

from datetime import datetime
import urllib
import urllib.request
import json
from IPython.display import display
from pkg_resources import ContextualVersionConflict

import sqlite3


class WeatherlinkConnection:

    # First, we define some class variables we will need again and again
    StationID = 0
    StationName = ""
    API_key = ""
    API_secret = ""

    Weather_Database = ""
    DB_FileName = ""

    floatLastTempReceived = 0

    def __init__(self) -> None:
        print("\nInitializing weatherlink connection ...")

        # We basically do get some parameters from the configuration file.
        # We will use those to obtain the station ID.
        config_file = 'config.ini'
        config = ConfigParser()
        config.read(config_file)

        self.API_key = config['weatherstation']['api_key2']
        self.API_secret = config['weatherstation']['api_secret']
        self.DB_FileName = config['weatherDB']['db_name']


        t = int(time.time())
        message_to_hash = "api-key{}t{}".format(self.API_key, t)
        apiSignature = hmac.new(self.API_secret.encode('utf-8'),message_to_hash.encode('utf-8'),hashlib.sha256).hexdigest()
        stations_url = "https://api.weatherlink.com/v2/stations?api-key={}&t={}&api-signature={}".format(self.API_key, t, apiSignature)

        with urllib.request.urlopen(stations_url) as url:
            data = json.loads(url.read().decode())
            #print(json.dumps(data, indent=4, sort_keys=False))

        self.StationID = data['stations'][0]['station_id']
        self.SeationName = data['stations'][0]['station_name']

        print("Successfully connected to {} with ID: {}\n".format(self.StationName, self.StationID))


    def ConvertFahrenheitToCelcius(self, fahrenheit_value):
        celsius_value = ((fahrenheit_value)-32)*(5/9)
        return celsius_value

    def GetOutsideTemp(self):

        #print("Start reading outside temp ...")

        t = int(time.time())
        message_to_hash = "api-key{}station-id{}t{}".format(self.API_key, self.StationID, t)
        apiSignature = hmac.new(self.API_secret.encode('utf-8'),message_to_hash.encode('utf-8'),hashlib.sha256).hexdigest()
        current_url = "https://api.weatherlink.com/v2/current/{}?api-key={}&t={}&api-signature={}".format(self.StationID, self.API_key, t, apiSignature)

        with urllib.request.urlopen(current_url) as url:
            data_values = json.loads(url.read().decode())
            #print(json.dumps(data_values, indent=4, sort_keys=True))

        temp = data_values['sensors'][1]['data'][0]['temp']
        temp = self.ConvertFahrenheitToCelcius(temp)

        #print(temp)

        return t, temp

    def DumpDataToDB(self):

        # before we can write data to the database, we need to check, if the db exists or not.
        # we create a connection to our DB first and build a cursor that will help us to manipulate the content

        # Please mind, if the DB does not exist, this command will generate an empty database for us.
        conn = sqlite3.connect(self.DB_FileName)
        c = conn.cursor()

        # now, we will try to add data to our database
        # if that fails, we know, that we will have to generate the respective table first before we can add data
        try:
            time_UTC , temp_Celsius = self.GetOutsideTemp()
            if (temp_Celsius != self.floatLastTempReceived):
                c.execute("INSERT INTO outsideweatherdata VALUES (?, ?)",(time_UTC, temp_Celsius))
                print(time_UTC, temp_Celsius)
            else:
                print("Temperature did not change.")
            self.floatLastTempReceived = temp_Celsius
            conn.commit()


        except sqlite3.OperationalError as err:
            print("Failed to write data to db as no table existed ...")
            print("We will not create the table inside the database first ...")
            # will create table first and will THEN add data
            c.execute("""CREATE TABLE outsideweatherdata (
                time integer,
                outside_temp real
            )""")
            conn.commit()
            time_UTC , temp_Celsius = self.GetOutsideTemp()
            print(time_UTC, temp_Celsius)
            c.execute("INSERT INTO outsideweatherdata VALUES (?, ?)",(time_UTC, temp_Celsius))
            conn.commit()


        conn.close()

    def ReadDataFromDB(self):
        conn = sqlite3.connect(self.DB_FileName)
        c = conn.cursor()

        c.execute("SELECT * FROM outsideweatherdata")
        print(c.fetchall())


        conn.commit()
        conn.close()


    def DisplayDataInDB(self):

        print("Start Reading Data from DB to visualize ... ")
        conn = sqlite3.connect(self.DB_FileName)
        c = conn.cursor()


        query = c.execute("SELECT * FROM outsideweatherdata")
        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

        # this command will print the pandas dataframe that contains exactly what's inside the database
        # print(results)

        # The UTC timestamps might be efficient for DB storage, but those are hard to read for a human
        # Therefore, we do convert the UTC timestamps into a human-readable timestamp
        local_timezone = tzlocal.get_localzone()
        results['time'] = [pd.Timestamp(datetime.fromtimestamp(time, local_timezone).strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)")) for time in results.time]

        # let's not print the time-converted table
        #print(results)

        # let's
        results.set_index('time', inplace=True)
        # results.sort_index(inplace=True)
        print("This is the table of the data to be visualized: ")
        print(" ")
        display(results)

        results.loc[:, ['outside_temp']].plot(figsize=(10, 5))
        plt.grid()
        plt.show()


        conn.commit()
        conn.close()
