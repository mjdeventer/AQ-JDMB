# Here we use the bme280.py script to output every second a string with local datetime, air temperature, relative humidity and atmospheric pressure.
# bme280.py contains the functions and the settings to communcate with the sensor. The file was authored from Matt Hawkins and it can be downloaded from 
# 'wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py'.
# Information on how to connect, setup and run the sensor can be found here:
# https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/

import datetime as dt
import time
import bme280 as bme

while True:
  temperature, pressure,humidity = bme.readBME280All()
  output = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S,') + '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
    temperature,
    pressure,
    humidity)
  print(output)
  time.sleep(1)

