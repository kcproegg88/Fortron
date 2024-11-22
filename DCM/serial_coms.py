import serial


def serial_stuff(dcm):
        with serial.Serial(port='COM5', baudrate=115200, timeout=1) as ser:


            data = {"mode": 6, "Lower rate limit": 40, "Upper rate limit": 180, "MSR_IN": 120, "AVDELAY_IN": 150, "Atrial amplitude": 50, "Ventricular amplitude": 50,
                    "Atrial pulse width": 1, "Ventricular pulse width": 1, "Atrial sensitivity": 40,
                    "Ventricular sensitivity": 40, "ARP": 25, "VRP": 32, "PVARP": 32,
                    "ACTIVITY_THRESHOLD_IN": 4, "REACTION_TIME_IN": 30, "RESPONSE_FACTOR_IN": 8, "RECOVERY_TIME_IN": 5,
                    "SYNC_IN": 22, "FUNCTION_IN": 85,}
            
            print(data.values())
            data = [i for i in data.values()]

            print("period")
            byte_data = bytes(data)
            ser.write(byte_data)
            ser.close()