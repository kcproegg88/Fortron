import sys
import time
import serial
import serial.tools.list_ports
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer


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


def serial_comm(dcm, sync_in: int, func_in: int):
    with serial.Serial(port=dcm, baudrate=115200, timeout=1) as ser:
        all_parameters = {"mode": 16, "Lower rate limit": 40, "Upper rate limit": 180, "MSR_IN": 120, "AVDELAY_IN": 150,
                          "Atrial amplitude": 50, "Ventricular amplitude": 50, "Atrial pulse width": 1,
                          "Ventricular pulse width": 1, "Atrial sensitivity": 40, "Ventricular sensitivity": 40,
                          "ARP": 25, "VRP": 32, "PVARP": 32, "ACTIVITY_THRESHOLD_IN": 4, "REACTION_TIME_IN": 30,
                          "RESPONSE_FACTOR_IN": 8, "RECOVERY_TIME_IN": 5, "SYNC_IN": sync_in, "FUNCTION_IN": func_in}
        data = [i for i in all_parameters.values()]
        st = struct.Struct('<BBBBBBBBBBBBBBBBBBBB')
        byte_data = st.pack(*data)
        ser.write(byte_data)
        ser.flush()

        streceive = struct.Struct('<ffBBBBBBBBBB')
        received_data = ser.read(streceive.size)
        response = streceive.unpack(received_data)
        return response


class LiveGraphWidget(QWidget):
    def __init__(self, length=100):
        super().__init__()
        self.length = length
        self.y_min = 0.45
        self.y_max = 0.55
        self.init_ui()

        # Initialize data buffers
        self.atrial_data = [0.5] * length
        self.ventricle_data = [0.5] * length
        self.time_data = [0] * length  # Buffer for elapsed time in seconds

        self.start_time = time.time()  # Start time reference
        self.port_device = check_connection("000621000000")
        if not self.port_device:
            print("Device not connected. Exiting...")
            return

        self.timer_interval = length  # Update interval in ms

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        self.tabs.addTab(self.tab_1, "Atrial Line")
        self.tabs.addTab(self.tab_2, "Ventricular Line")
        self.tabs.addTab(self.tab_3, "Both Lines")

        self.tab_1_layout = QVBoxLayout(self.tab_1)
        self.tab_2_layout = QVBoxLayout(self.tab_2)
        self.tab_3_layout = QVBoxLayout(self.tab_3)


        self.figure_1, self.ax_1 = plt.subplots()
        self.canvas_1 = FigureCanvas(self.figure_1)
        self.figure_2, self.ax_2 = plt.subplots()
        self.canvas_2 = FigureCanvas(self.figure_2)
        self.figure_3, self.ax_3 = plt.subplots()
        self.canvas_3 = FigureCanvas(self.figure_3)

        self.tab_1_layout.addWidget(self.canvas_1)
        self.tab_2_layout.addWidget(self.canvas_2)
        self.tab_3_layout.addWidget(self.canvas_3)

        # Initialize plot lines
        self.atrial_line_1, = self.ax_1.plot([], [], label="Atrial", color="blue")
        self.ventrical_line_2, = self.ax_2.plot([], [], label="Ventricular", color="red")
        self.atrial_line_3, = self.ax_3.plot([], [], label="Atrial", color="blue")
        self.ventrical_line_3, = self.ax_3.plot([], [], label="Ventricular", color="red")

        # Configure plot
        self.ax_1.set_xlim(0, int(self.length/10))  # Initially show the first 5 seconds
        self.ax_1.set_ylim(self.y_min, self.y_max)
        self.ax_1.legend()
        self.ax_1.set_title("Live Atrial Data Over Time")
        self.ax_1.set_xlabel("Time (s)")
        self.ax_1.set_ylabel("Signal")

        self.ax_2.set_xlim(0, int(self.length / 10))  # Initially show the first 5 seconds
        self.ax_2.set_ylim(self.y_min, self.y_max)
        self.ax_2.legend()
        self.ax_2.set_title("Live Ventricular Data Over Time")
        self.ax_2.set_xlabel("Time (s)")
        self.ax_2.set_ylabel("Signal")

        self.ax_3.set_xlim(0, int(self.length / 10))  # Initially show the first 5 seconds
        self.ax_3.set_ylim(self.y_min, self.y_max)
        self.ax_3.legend()
        self.ax_3.set_title("Live Atrial and Ventricular Data Over Time")
        self.ax_3.set_xlabel("Time (s)")
        self.ax_3.set_ylabel("Signal")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        buttons_layout = QHBoxLayout()
        # Add Start and Pause buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_live_plot)
        buttons_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_live_plot)
        buttons_layout.addWidget(self.pause_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def update_plot(self):
        try:
            # Retrieve atrial and ventricular data from serial_comm
            data = serial_comm(self.port_device, 22, 56)
            atrial, ventricle = data[0], data[1]

            # Update time data with the current elapsed time
            elapsed_time = time.time() - self.start_time
            self.time_data.append(elapsed_time)
            self.time_data.pop(0)

            # Update data buffers
            self.atrial_data.append(atrial)
            self.ventricle_data.append(ventricle)
            self.atrial_data.pop(0)
            self.ventricle_data.pop(0)

            # Update plot lines
            self.atrial_line_1.set_data(self.time_data, self.atrial_data)
            self.ventrical_line_2.set_data(self.time_data, self.ventricle_data)
            self.atrial_line_3.set_data(self.time_data, self.atrial_data)
            self.ventrical_line_3.set_data(self.time_data, self.ventricle_data)

            # Adjust Y-axis dynamically
            self.y_min = min(self.y_min, atrial, ventricle)
            self.y_max = max(self.y_max, atrial, ventricle)
            self.ax_1.set_ylim(self.y_min - 0.01, self.y_max + 0.01)
            self.ax_2.set_ylim(self.y_min - 0.01, self.y_max + 0.01)
            self.ax_3.set_ylim(self.y_min - 0.01, self.y_max + 0.01)

            # Adjust X-axis to show only the latest values (last length/10 seconds)
            if self.time_data[-1] > int(self.length/10):  # Adjust to last length/10 seconds dynamically
                self.ax_1.set_xlim(self.time_data[-1] - int(self.length/10), self.time_data[-1])
                self.ax_2.set_xlim(self.time_data[-1] - int(self.length/10), self.time_data[-1])
                self.ax_3.set_xlim(self.time_data[-1] - int(self.length/10), self.time_data[-1])

            # Redraw the canvas
            self.canvas_1.draw()
            self.canvas_2.draw()
            self.canvas_3.draw()

        except Exception as e:
            print(f"Error during plotting: {e}")

    def start_live_plot(self):
        self.timer = QTimer(self)
        self.timer.setInterval(self.timer_interval)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def pause_live_plot(self):
        if self.timer is not None:  # If the timer exists, stop it
            self.timer.stop()
            self.timer = None  # Reset timer so it can be restarted later

    def stop_live_plot(self):
        # Stop the timer and cleanup
        if self.timer is not None:
            self.timer.stop()
            self.timer = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.live_graph_widget = LiveGraphWidget()
        self.setCentralWidget(self.live_graph_widget)
        self.setWindowTitle("Live Atrial and Ventricular Data")
        self.resize(800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
