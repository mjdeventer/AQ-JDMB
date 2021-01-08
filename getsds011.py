import time, struct
import pandas as pd
import serial

def getsds011(comport):
    """Opens COM to SDS011 and returns 1 data touple of PM25 and PM10
    input - string of the comport the SDS011 is connected to
    output - a 1x2 toubple with [0] entry being pm25 and [1] being pm10"""
    
    portflagsds011 = True
    ser = serial.Serial()
    ser.port = comport # Set this to your serial port
    ser.baudrate = 9600
    ser.open()
    ser.flushInput()
    byte, lastbyte = "\x00", b'\xab'
    while portflagsds011== True:
        #lastbyte = byte
        byte = ser.read(size=1); #print(byte)
        
        # We got a valid packet header
        if byte == b'\xc0' and lastbyte == b'\xab':
        #if lastbyte == "\x00" and byte == b'\xaa':
            sentence = ser.read(size=8) # Read 8 more bytes
            readings = struct.unpack('<hhxxcc',sentence) # Decode the packet - little endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail
            
            pm_25 = readings[0]/10
            pm_10 = readings[1]/10
            # ignoring the checksum and message tail
            
            print("PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3")
            lastbyte = readings[3]
            del readings
            portflagsds011 = False
            #ser.flushInput()
            ser.close()
            return pm_25, pm_10
