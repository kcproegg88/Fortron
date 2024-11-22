import serial


def serial_stuff(dcm):
        with serial.Serial(port='COM5', baudrate=115200, timeout=1) as ser:

            ser = serial.Serial(port='COM5', baudrate=115200, timeout=1)


            data = {"mode": 1, "Lower rate limit": 2, "Upper rate limit": 3, "MSR_IN": 120, "AVDELAY_IN": 150, "Atrial amplitude": 50, "Ventricular amplitude": 5,
                    "Atrial pulse width": 5, "Ventricular pulse width": 5, "Atrial sensitivity": 25,
                    "Ventricular sensitivity": 11, "ARP": 15, "VRP": 15, "PVARP": 15,
                    "ACTIVITY_THRESHOLD_IN": 4, "REACTION_TIME_IN": 30, "RESPONSE_FACTOR_IN": 8, "RECOVERY_TIME_IN": 5,
                    "SYNC_IN": 22, "FUNCTION_IN": 85,}

            data["mode"] = dcm.main_page.params_stacked_widget.currentIndex()
            data[0] = dcm.main_page.params_stacked_widget.currentIndex()  # Mode


            print("period")
            byte_data = bytes(data.values())
            ser.write(byte_data)
            ser.close()