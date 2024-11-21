import serial

def serial_stuff(dcm):
        with serial.Serial(port='COM5', baudrate=115200, timeout=1) as ser:

            ser = serial.Serial(port='COM5', baudrate=115200, timeout=1)


            data = {"mode": 1, "Lower rate limit": 2, "Upper rate limit": 3, "MSR_IN": 4, "AVDELAY_IN": 5, "ATRIUM_AMP_IN": 6, "VENTRICLE_AMP_IN": 7,
                    "ATRIUM_PULSE_WIDTH_IN": 8, "VENTRICLE_PULSE_WIDTH_IN": 9, "ATRIUM_SENSITIVITY_IN": 10,
                    "VENTRICLE_SENSITIVITY_IN": 11, "ATRIUM_RP_IN": 12, "VENTRICLE_RP_IN": 13, "PV_ARP_IN": 14,
                    "ACTIVITY_THRESHOLD_IN": 15, "REACTION_TIME_IN": 16, "RESPONSE_FACTOR_IN": 17, "RECOVERY_TIME_IN": 18,
                    "SYNC_IN": 19, "FUNCTION_IN": 20,}

            data["mode"] = dcm.main_page.params_stacked_widget.currentIndex()
            data[0] = dcm.main_page.params_stacked_widget.currentIndex()  # Mode
            data[5] = 0  # Example: Placeholder
            data[18] = 22  # Example: Recovery time
            data[19] = 85  # Example: Checksum or termination byte

            print("period")
            byte_data = bytes(data.values())
            ser.write(byte_data)
            ser.close()