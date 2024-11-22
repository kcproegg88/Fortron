import serial.tools.list_ports


def get_connected_ports():
    # Retrieve a list of all available ports
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No COM ports found.")
        return []

    connected_ports = []
    for port in ports:
        port_name = port.device
        description = port.description
        hwid = port.hwid
        connected_ports.append((port_name, description, hwid))

    return connected_ports


# Example usage
connected_ports = get_connected_ports()
if connected_ports:
    print("Connected COM Ports:")
    for port_name, description, hwid in connected_ports:
        print(f"Port: {port_name}, Description: {description}, HWID: {hwid}")
else:
    print("No serial ports are currently connected.")
