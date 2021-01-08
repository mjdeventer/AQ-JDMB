# -*- coding: utf-8 -*- 
import time, struct
import pandas as pd
import serial
import bme280 as bme
import datetime as dt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from getsds011 import *

### Instantiate the connection to the InfluxDB client."""
user = 'INSERT_YOUR_EMAIL_HERE';
password = 'INSERT_YOUR_PW_HERE'
dbname = 'AQ-JDMB'
protocol = 'line'
token = "1kn0mBd9TSX9ZFSjAC-U4SpZUFPrl7kYja9sPiGVAxSEnU7lu_r6oxDv2dkRO-eWrz1fpTeY1O78HmpbFlRUtA=="
bucket = "AQ-JDMB"
siteid = "Bundesstr" #use 'Bundesstr', or 'Goettingen' tag for influxdb
client = InfluxDBClient(url="https://westeurope-1.azure.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


comsds011 = "/dev/ttyUSB0"
#dfaq = pd.DataFrame({'DateTime':[dt.datetime.now()],'PM25':[0],'PM10':[0]}) #preallocating DF for logger storage, adapt to your sensors and readouts
dfaq = pd.DataFrame({'DateTime':[dt.datetime.now()],'PM10':[0],'PM25':[0],'Ta':[0],'Pa':[0],'RH':[0]}) 

starttime = time.time()
starttimestr = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
loggstep = 3 # in seconds
i = 0
while True:
    pmout = getsds011(comsds011) #insert function to call any sensor here 
    bmeout = bme.readBME280All()
    print('Ta = '+str(round(bmeout[0],1)) + 'RH = '+str(round(bmeout[2],1)))
    newdata = [{'DateTime':dt.datetime.now(),'PM25':pmout[0],'PM10':pmout[1],'Ta':round(bmeout[0],1),'Pa':round(bmeout[1],3),'RH':round(bmeout[2],1)}]
    dfaq = dfaq.append(newdata,ignore_index = True);
    del newdata; #del pmout; del bmeout
    print("appended new data to Logger DF")
    time.sleep(loggstep - ((time.time() - starttime) % loggstep))
    newtime = time.time()
    if (newtime>(starttime + (60*i))):
        dfaq.to_csv(starttimestr+'_logger.csv')
        print("wrote file")
        i = i+1
        data = "Temperature,host=bme280,location="+siteid+" Air="+str(round(bmeout[0],1))
        write_api.write(bucket, user, data)
        data = "Humidity,host=bme280,location="+siteid+" Air="+str(round(bmeout[2],0))
        write_api.write(bucket, user, data)
        data = "Pressure,host=bme280,location="+siteid+" Air="+str(round(bmeout[1]/100,0))
        write_api.write(bucket, user, data)
        data = "PM10,host=SDS011,location="+siteid+" Air="+str(round(pmout[1],1))
        write_api.write(bucket, user, data)
        data = "PM25,host=SDS011,location="+siteid+" Air="+str(round(pmout[0],1))
        write_api.write(bucket, user, data)
        print("...wrote data to influxdb")
