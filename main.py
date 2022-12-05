import weatherlink_connect
import time

# First, we will try to reach the Weatherlink WeatherStation:
WLL = weatherlink_connect.WeatherlinkConnection()

#WLL.GetOutsideTemp()

try:
    while True:
        WLL.DumpDataToDB()
        time.sleep(60)
except KeyboardInterrupt:
    pass

# WLL.DumpDataToDB()
#WLL.ReadDataFromDB()
WLL.DisplayDataInDB()
