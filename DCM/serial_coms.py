import serial

import serial

ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)

data = [i for i in range(20)]
byte_data = bytes(data)
ser.write(byte_data)
ser.close()