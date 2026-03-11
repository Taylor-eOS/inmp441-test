import serial
import numpy as np
import matplotlib.pyplot as plt

ser=serial.Serial('/dev/ttyACM0',921600)

while True:
    data=ser.read(4096)
    samples=np.frombuffer(data,dtype=np.int32)
    samples=samples>>8
    print("min",samples.min(),"max",samples.max())
