import serial
import serial.tools.list_ports
import struct
import time
import matplotlib.pyplot as plt


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
    # Check connection with the specific device
    port = check_connection("000621000000")
    if port == 0:
        return 0

    try:
        # Open the serial connection
        with serial.Serial(port=port, baudrate=115200, timeout=1) as ser:
            # Parameters to be sent
            all_parameters = {
                "mode": 16, "Lower rate limit": 40, "Upper rate limit": 180, "MSR_IN": 120, "AVDELAY_IN": 150,
                "Atrial amplitude": 50, "Ventricular amplitude": 50, "Atrial pulse width": 1,
                "Ventricular pulse width": 1, "Atrial sensitivity": 40, "Ventricular sensitivity": 40,
                "ARP": 25, "VRP": 32, "PVARP": 32, "ACTIVITY_THRESHOLD_IN": 4, "REACTION_TIME_IN": 30,
                "RESPONSE_FACTOR_IN": 8, "RECOVERY_TIME_IN": 5, "SYNC_IN": 22, "FUNCTION_IN": 56
            }

            # Prepare the data to send
            data = [i for i in all_parameters.values()]
            print("Data to send:", data)
            # Send the data as bytes
            st = struct.Struct('<BBBBBBBBBBBBBBBBBBBB')
            byte_data = st.pack(*data)

            # Initialize Matplotlib
            plt.ion()  # Interactive mode on
            fig, ax = plt.subplots()
            atrial_line, = ax.plot([], [], label="Atrial", color="blue")
            ventrical_line, = ax.plot([], [], label="Ventricular", color="red")
            ax.set_xlim(0, 50)  # Adjust X-axis limit
            ax.set_ylim(0, 300)  # Adjust Y-axis limit (byte values are 0-255)
            ax.set_xlabel("Time (frames)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            plt.title("Real-Time Atrial and Ventricular Signals")

            atrial_data = []
            ventricular_data = []
            frames = []


            while True:
                ser.write(byte_data)
                print("Data written successfully.", byte_data)

                # Wait briefly for the device to respond
                ser.flush()

                # Read response from the device
                streceive = struct.Struct('<ffBBBBBBBBBB')
                received_data = ser.read(streceive.size)
                unpacked_data = streceive.unpack(received_data)
                response = ser.read(18)  # Adjust the number of bytes to read as needed
                print("Response received:", response)
                translated = list(response)
                print(f"Translated Response: {translated}")

                # Extract Atrial and Ventricular data
                atrial = translated[0] # Sum of first 4 bytes for simplicity
                ventricular = translated[4]  # Sum of next 4 bytes

                # Update data lists
                frames.append(len(frames))
                atrial_data.append(atrial)
                ventricular_data.append(ventricular)

                # Update Matplotlib plot
                atrial_line.set_data(frames, atrial_data)
                ventrical_line.set_data(frames, ventricular_data)

                # Adjust X-axis dynamically
                ax.set_xlim(max(0, len(frames) - 50), len(frames))

                ax.relim()
                ax.autoscale_view()
                plt.draw()
                plt.pause(0.01)  # Pause briefly for the plot to update

                time.sleep(0.5)
            # Close the connection

            #atrial is first 4 and ventrical is next 4
            plt.ioff()  # Turn off interactive mode
            plt.show()
            ser.close()
            ser.close()
            return response

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

response = serial_stuff("dummy")
if response:
    print("Final Response:", response)
else:
    print("No response or failed communication.")