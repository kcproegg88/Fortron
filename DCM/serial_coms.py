import serial
import serial.tools.list_ports


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


def serial_stuff(dcm):
    port = check_connection("000621000000")
    if port == 0:
        return 0

    with serial.Serial(port=port, baudrate=115200, timeout=1) as ser:
        all_parameters = {"mode": 6, "Lower rate limit": 40, "Upper rate limit": 180, "MSR_IN": 120, "AVDELAY_IN": 150,
                          "Atrial amplitude": 50, "Ventricular amplitude": 50, "Atrial pulse width": 1,
                          "Ventricular pulse width": 1, "Atrial sensitivity": 40, "Ventricular sensitivity": 40,
                          "ARP": 25, "VRP": 32, "PVARP": 32, "ACTIVITY_THRESHOLD_IN": 4, "REACTION_TIME_IN": 30,
                          "RESPONSE_FACTOR_IN": 8, "RECOVERY_TIME_IN": 5, "SYNC_IN": 22, "FUNCTION_IN": 85}

        data = [i for i in all_parameters.values()]

        print(data)

        print("period")
        byte_data = bytes(data)
        ser.write(byte_data)
        ser.close()