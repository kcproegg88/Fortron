import serial

import serial

ser = serial.Serial(port='COM5', baudrate=115200, timeout=1)

data = [i for i in range(20)]
data[5] = 0
data[0] = 0
data[19] = 85
data[18] = 22 
print("period")
byte_data = bytes(data)
ser.write(byte_data)
ser.close()