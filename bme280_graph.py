# This file extends the functionality of the bme280.py script including a real-time plot of the measuring variable.
# This code has been created using the resources found here: 'https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/all#update-a-graph-in-real-time'


import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bme280 as bme


