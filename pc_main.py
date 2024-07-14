#!/usr/bin/env python
# coding: utf-8

# In[15]:


#main Python script

import GPUtil
import psutil
import wmi
import math
import serial
import time


def write_read(x): #function to send data to the arduino board
    arduino.write(bytes(x,'utf-8'))


#while 1:
w = wmi.WMI(namespace="root\OpenHardwareMonitor") #open Hardware Monitor
temperature_infos = w.Sensor()
value=0

for sensor in temperature_infos: #Search for the CPU temperature. Due to lack of OpenHardwareMonitor limitation with 11th Intel Family I only get the core 0 temp.
#It is posible to do the mean of all your processor temps. 
  if sensor.SensorType==u'Temperature' and sensor.Parent==u'/lpc/nct6798d' and sensor.Name==u'Temperature #1':
      value=sensor.Value

gpu = GPUtil.getGPUs()[0]

A = str(round(value,2))
B = str(round(psutil.cpu_percent(),2))
C = str(round(gpu.temperature,2))
D = str(round(gpu.load*100,2))
finalString = 'CPU: '+A + "," + B + "_GPU: " + C + "," + D + "\n" #Create the String to send to arduino
print(finalString) #calling the send function


# In[ ]:


# Update this to your actual serial port
serial_port = 'COM31'  # e.g., 'COM3' for Windows or '/dev/ttyUSB0' for Linux/Mac

# Configure the serial port with 115200 baud rate
try:
    ser = serial.Serial(serial_port, 115200, timeout=1)
    print(f"Connected to {serial_port}")
except serial.SerialException as e:
    print(f"Error: {e}")
    sys.exit(1)

time.sleep(0.3)  # Give some time for the connection to establish

def get_gpu_power_utilization():
    power_value = 0
    for sensor in temperature_infos:
        if sensor.SensorType == u'Power':
            #print (sensor)#and 'gpu' in sensor.Parent.lower():
            
            power_value = sensor.Value
            
    return str(int(power_value))+'W'

def send_string(data):
    ser.write(data.encode() + b'\n')  # Ensure the data ends with a newline
    ser.flush()  # Ensure the data is sent
    print(f"Sent: {data}")

try:
    while(1):
        
        w = wmi.WMI(namespace="root\OpenHardwareMonitor") #open Hardware Monitor
        temperature_infos = w.Sensor()
        value=0

        for sensor in temperature_infos: #Search for the CPU temperature. Due to lack of OpenHardwareMonitor limitation with 11th Intel Family I only get the core 0 temp.
        #It is posible to do the mean of all your processor temps. 
          if sensor.SensorType==u'Temperature' and sensor.Parent==u'/lpc/nct6798d' and sensor.Name==u'Temperature #1':
              value=sensor.Value

        gpu = GPUtil.getGPUs()[0]

        A = str(int(value))
        B = str(int(psutil.cpu_percent()))
        C = str(int(gpu.temperature))
        D = str(int(round(gpu.load*100,0)))
        E = get_gpu_power_utilization()
        finalString = 'CPU:'+A + "C " + B + "%_GPU:" + C + "C " + D + "% "+E+"\n" #Create the String to send to arduino
        print(finalString) #calling the send function
        send_string(finalString)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()






