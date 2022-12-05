import weatherlink_live_local as wlll
import time

devices = wlll.discover()
print(devices)

# string APIkey = p8gfl0ndkve9ydlpi9elxq3hkwkszt1a
# string APIsecret = fhrwrkawzyonkd3ppubd1zpjrkypsw24
# string timestampe = 123456

# select first device, get IP address
ip_first_device = devices[0].ip_addresses[0]

# specify units
wlll.set_units(
    temperature=wlll.units.TemperatureUnit.CELSIUS,
    pressure=wlll.units.PressureUnit.HECTOPASCAL,
    rain=wlll.units.RainUnit.MILLIMETER,
    wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND,
)

# poll sensor data / conditions
while True:
    conditions = wlll.get_conditions(ip_first_device)
    print(f"Inside temperature:  {conditions.inside.temp:.2f} °C")
    print(
        f"Outside temperature: {conditions.integrated_sensor_suites[0].temp:.2f} °C"
    )
    time.sleep(10)