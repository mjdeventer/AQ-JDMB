# This file extends the functionality of the bme280.py script including a real-time plot of the measuring variable.
# This code has been created using the tutorial found at sparkfun at the following address: 
# 'https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/all#update-a-graph-in-real-time'

# Import libraries
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bme280 as bme

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xs = []
ys = []

def animate(i, xs, ys):
  temperature = bme.readBME280All()
  temp_c = temperature[0]
  
  # Add x and y to lists
  xs.append(dt.datetime.now().strftime('%H:%M:%S'))
  ys.append(temp_c)
  
  # Limit x and y lists to 20 items
  xs = xs[-20:]
  ys = ys[-20:]
  
  # Draw x and y lists
  ax.clear()
  ax.plot(xs, ys)
  
  # Format plot
  plt.xticks(rotation=45, ha='right')
  plt.subplots_adjust(bottom=0.30)
  plt.title('BME280 Temperature vs. Time')
  plt.ylabel('Temperature (°C)')
 
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
    


