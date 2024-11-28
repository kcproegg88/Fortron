import serial
import serial.tools.list_ports
import struct


def check_connection(ser_num):
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No COM ports found.")
        return None
    for port in ports:
        if not port.hwid:
            continue
        if f"SER={ser_num}" in port.hwid.split():
            return port.device
    print("Device Not Found")
    return None


def serial_comm(port_name, sync_in: int, func_in: int, parameters=None, mode=16):
    with serial.Serial(port=port_name, baudrate=115200, timeout=1) as ser:
        all_parameters = {"mode": mode, "Lower rate limit": 40, "Upper rate limit": 180, "Maximum Sensor Rate": 120, "AVDELAY_IN": 150,
                          "Atrial amplitude": 50, "Ventricular amplitude": 50, "Atrial pulse width": 1,
                          "Ventricular pulse width": 1, "Atrial sensitivity": 40, "Ventricular sensitivity": 40,
                          "ARP": 25, "VRP": 32, "PVARP": 32, "Activity Threshold": 3, "Reaction Time": 30,
                          "Response Factor": 8, "Recovery Time": 5, "SYNC_IN": sync_in, "FUNCTION_IN": func_in}
        if parameters:
            for parameter in parameters:
                all_parameters[parameter] = parameters[parameter]
            print(f"in the function: {all_parameters}")
        data = [i for i in all_parameters.values()]
        st = struct.Struct('<BBBBBBBBBBBBBBBBBBBB')
        byte_data = st.pack(*data)
        ser.write(byte_data)
        ser.flush()
        if not all_parameters["FUNCTION_IN"] == 85:
            if parameters:
                streceive = struct.Struct('<BBBBBBBBBBBBBB')
            else:
                streceive = struct.Struct('<ffBBBBBBBBBB')
            received_data = ser.read(streceive.size)
            try:
                response = streceive.unpack(received_data)
                return response
            except Exception as e:
                print(f"serial comms error: {e}")
                print(received_data)
