from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
from serial_coms import check_connection, serial_comm


class LiveGraphWidget(QWidget):
    def __init__(self, dcm, length=50):
        super().__init__()
        self.dcm = dcm
        self.length = length
        self.y_min = 0.49
        self.y_max = 0.51
        self.init_ui()

        # Initialize data buffers
        self.atrial_data = [0.5] * length
        self.ventricle_data = [0.5] * length
        self.time_data = [0] * length  # Buffer for elapsed time in seconds

        self.port_device = check_connection(self.dcm.pacemaker_serial)

        self.timer_interval = length  # Update interval in ms

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        self.tabs.addTab(self.tab_3, "Both Lines")
        self.tabs.addTab(self.tab_1, "Atrial Line")
        self.tabs.addTab(self.tab_2, "Ventricular Line")

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

        # Add Start, Save and Pause buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_live_plot)
        buttons_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_live_plot)
        buttons_layout.addWidget(self.pause_button)

        self.save_button = QPushButton("Save Graph")
        self.save_button.clicked.connect(self.save_graph)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)
        self.timer = QTimer(self)
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

            self.dcm.main_page.comm_status.setText("Receiving ECG Data")
            self.dcm.main_page.comm_status.setStyleSheet("color: green;")

        except Exception as e:
            self.dcm.main_page.comm_status.setText("ECG Interrupted")
            self.dcm.main_page.comm_status.setStyleSheet("color: red;")
            self.reset_live_plot()
            print(f"Error during plotting: {e}")

    def start_live_plot(self):
        self.port_device = check_connection(self.dcm.pacemaker_serial)
        if not self.port_device:
            self.dcm.main_page.device_status.setText("No Device Detected")
            self.dcm.main_page.device_status.setStyleSheet("color: red;")
            print("Device not connected. Exiting...")
        else:
            self.dcm.main_page.device_status.setText(f"Connected: {self.port_device}")
            self.dcm.main_page.device_status.setStyleSheet("color: green;")
        self.reset_live_plot()
        self.timer = QTimer(self)
        self.start_time = time.time()  # Start time reference
        self.timer.setInterval(self.timer_interval)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def pause_live_plot(self):
        if self.timer is not None:  # If the timer exists, stop it
            self.timer.stop()
            self.timer = None  # Reset timer so it can be restarted later

        self.dcm.main_page.comm_status.setText("No Data Transfer")
        self.dcm.main_page.comm_status.setStyleSheet("color: grey;")

    def reset_live_plot(self):
        self.pause_live_plot()
        # Clear data buffers
        self.y_min = 0.49
        self.y_max = 0.51
        self.time_data = [0] * self.length
        self.atrial_data = [0.5] * self.length
        self.ventricle_data = [0.5] * self.length

        # Reset plot limits
        self.ax_1.set_xlim(0, int(self.length / 10))
        self.ax_1.set_ylim(self.y_min, self.y_max)
        self.ax_2.set_xlim(0, int(self.length / 10))
        self.ax_2.set_ylim(self.y_min, self.y_max)
        self.ax_3.set_xlim(0, int(self.length / 10))
        self.ax_3.set_ylim(self.y_min, self.y_max)

        # Clear existing plot lines
        self.atrial_line_1.set_data([], [])
        self.ventrical_line_2.set_data([], [])
        self.atrial_line_3.set_data([], [])
        self.ventrical_line_3.set_data([], [])

        # Update canvas
        self.canvas_1.draw()
        self.canvas_2.draw()
        self.canvas_3.draw()

    def save_graph(self):
        try:
            self.figure_1.savefig(f"atrial_file.png", format="png")
            self.figure_2.savefig(f"ventricular_file.png", format="png")
            self.figure_3.savefig(f"ecg_file.png", format="png")
        except Exception as e:
            print(f"Error saving: {e}")
