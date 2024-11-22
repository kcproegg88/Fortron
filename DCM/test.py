import serial
import serial.tools.list_ports
import time


def check_connection(ser_num):
    # Retrieve a list of all available ports
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No COM ports found.")
        return 0

    for port in ports:
        if not port.hwid:
            continue
        print(f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}")
        if f"SER={ser_num}" in port.hwid.split():
            return port.device

    print("Device Not Found")
    return 0


def serial_receive():
    port = check_connection("000621000000")
    if port == 0:
        return 0
    with serial.Serial(port=port, baudrate=115200, timeout=1) as ser:
        while True:
            if ser.in_waiting > 0:  # Check if data is available to read
                data = ser.readline()  # Read a line of data
                print("Received:", data.decode('utf-8').strip())  # Print received data

            time.sleep(0.1)  # Small delay to prevent excessive CPU

try:
    serial_receive()
except KeyboardInterrupt:
    print("Program interrupted")