# -*- coding: utf-8 -*- 
import time, struct
import pandas as pd
import serial
import bme280 as bme
import Adafruit_DHT
import datetime as dt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from getsds011 import *

### Instantiate the connection to the InfluxDB client."""
user = 'maju.deventer@googlemail.com';
password = 'Lnf-Leinefelde'
dbname = 'AQ-JDMB'
protocol = 'line'
token = "1kn0mBd9TSX9ZFSjAC-U4SpZUFPrl7kYja9sPiGVAxSEnU7lu_r6oxDv2dkRO-eWrz1fpTeY1O78HmpbFlRUtA=="
bucket = "AQ-JDMB"
siteid = "Goettingen" #use 'Bundesstr', or 'Goettingen' tag for influxdb
client = InfluxDBClient(url="https://westeurope-1.azure.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Local path to store the data
local_path = "/home/pi/AQ_monitor/Data/"
# USB port where the SDS011 is connected to the Pi
comsds011 = "/dev/ttyUSB0"
# Definition of the DHT22 Sensor 
DHT_SENSOR = Adafruit_DHT.DHT22
# Set the GPIO pin of the Pi where the DHT22 is connected to
DHT_PIN = 4
#dfaq = pd.DataFrame({'DateTime':[dt.datetime.now()],'PM25':[0],'PM10':[0]}) #preallocating DF for logger storage, adapt to your sensors and readouts
dfaq = pd.DataFrame({'DateTime':[dt.datetime.now()],'PM10':[0],'PM25':[0],'Ta_int':[0],'Ta_ext':[0],'Pa':[0],'RH_int':[0],'RH_ext':[0]}) 

starttime = time.time()
starttimestr = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
loggstep = 3 # in seconds
i = 0
while True:
    # Call for SDS011
    pmout = getsds011(comsds011) #insert function to call any sensor here
    # Call for BME280
    bmeout = bme.readBME280All()
    # Call for DHT22
    dhtout = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    print(bmeout[0],dhtout[1],bmeout[2],dhtout[0])
    '''
    # Print a string showing the current data 
    print('Ta_int = '+str(round(bmeout[0],1)) + ' RH_int = '+str(round(bmeout[2],1)) + ' Press = '+str(round(bmeout[1],2)) +
          ' Ta_ext = '+str(round(dhtout[1],1)) + ' RH_ext = '+str(round(dhtout[0],1)) +
          ' PM25 = '+str(round(pmout[0],1)) + ' PM10 = '+str(round(pmout[1],1)))
    
    # Create dataframe and send the data to the InfluxDB server.
    # Copy the data into a daily local file  
    newdata = [{'DateTime':dt.datetime.now(),'PM25':pmout[0],'PM10':pmout[1],'Ta_int':round(bmeout[0],1),'Ta_ext':round(dhtout[1],1),'Press':round(bmeout[1],3),'RH_int':round(bmeout[2],1),'RH_ext':round(dhtout[0],1)}]
    dfaq = dfaq.append(newdata,ignore_index = True);
    del newdata; #del pmout; del bmeout
    print("appended new data to Logger DF")
    time.sleep(loggstep - ((time.time() - starttime) % loggstep))
    newtime = time.time()
    if (newtime>(starttime + (60*i))):
        dfaq.to_csv(local_path + starttimestr + '_logger.csv')
        print("wrote file")
        i = i+1
        data = "Temperature,host=bme280,location="+siteid+" Air="+str(round(bmeout[0],1))
        write_api.write(bucket, user, data)
        data = "Humidity,host=bme280,location="+siteid+" Air="+str(round(bmeout[2],1))
        write_api.write(bucket, user, data)
        data = "Pressure,host=bme280,location="+siteid+" Air="+str(round(bmeout[1],1))
        write_api.write(bucket, user, data)
        data = "Temperature_Ext,host=DHT22,location="+siteid+" Air="+str(round(dhtout[1],1))
        write_api.write(bucket, user, data)
        data = "Humidity_Ext,host=DHT22,location="+siteid+" Air="+str(round(dhtout[0],1))
        write_api.write(bucket, user, data)        
        data = "PM10,host=SDS011,location="+siteid+" Air="+str(round(pmout[1],1))
        write_api.write(bucket, user, data)
        data = "PM25,host=SDS011,location="+siteid+" Air="+str(round(pmout[0],1))
        write_api.write(bucket, user, data)
        print("...wrote data to influxdb")
'''