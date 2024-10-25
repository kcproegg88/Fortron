from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton, QSlider, QStackedWidget
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QPixmap
from parameter_display import PaceMakerMode

class MainPage():
    def __init__(self, dcm):
        self.dcm = dcm
        self.params_stacked_widget = QStackedWidget()
        modes = ["AOO", "VOO", "AAI", "VVI"]

        # AOO Mode Parameters
        mode_widget = PaceMakerMode("AOO", self.dcm, [
            ["Lower rate limit", 30, 175, 1],  # (30-175 ppm)
            ["Upper rate limit", 50, 175, 1],  # (50-175 ppm)
            ["Atrial amplitude", 5, 32, 10],  # (0.5-3.2V)
            ["Atrial pulse width", 5, 190, 100]  # (0.05-1.9 ms)
        ])
        self.params_stacked_widget.addWidget(mode_widget)
        self.dcm.mode["AOO"] = mode_widget

        # VOO Mode Parameters
        mode_widget = PaceMakerMode("VOO", self.dcm, [
            ["Lower rate limit", 30, 175, 1],  # (30-175 ppm)
            ["Upper rate limit", 50, 175, 1],  # (50-175 ppm)
            ["Ventricular amplitude", 5, 32, 10],  # (0.5-3.2V)
            ["Ventricular pulse width", 5, 190, 100]  # (0.05-1.9 ms)
        ])
        self.params_stacked_widget.addWidget(mode_widget)
        self.dcm.mode["VOO"] = mode_widget

        # AAI Mode Parameters
        mode_widget = PaceMakerMode("AAI", self.dcm, [
            ["Lower rate limit", 30, 175, 1],  # (30-175 ppm)
            ["Upper rate limit", 50, 175, 1],  # (50-175 ppm)
            ["Atrial amplitude", 5, 32, 10],  # (0.5-3.2V)
            ["Atrial pulse width", 5, 190, 100],  # (0.05-1.9 ms)
            ["Atrial sensitivity", 25, 1000, 100],  # (0.25-10 mV)
            ["ARP", 150, 500, 1],  # (150-500 ms)
            ["PVARP", 150, 500, 1]  # (150-500 ms)
        ])
        self.params_stacked_widget.addWidget(mode_widget)
        self.dcm.mode["AAI"] = mode_widget

        # VVI Mode Parameters
        mode_widget = PaceMakerMode("VVI", self.dcm, [
            ["Lower rate limit", 30, 175, 1],  # (30-175 ppm)
            ["Upper rate limit", 50, 175, 1],  # (50-175 ppm)
            ["Ventricular amplitude", 5, 32, 10],  # (0.5-3.2V)
            ["Ventricular pulse width", 5, 190, 100],  # (0.05-1.9 ms)
            ["Ventricular sensitivity", 25, 1000, 100],  # (0.25-10 mV)
            ["VRP", 150, 500, 1],  # (150-500 ms)
            ["Hysteresis interval", 200, 500, 1],  # (200-500 ms)
            ["Low rate interval", 343, 2000, 1]  # (343-2000 ms)
        ])
        self.params_stacked_widget.addWidget(mode_widget)
        self.dcm.mode["VVI"] = mode_widget

        self.layout = QVBoxLayout()  # Main layout

        # Title
        title = QLabel("DCM Main Interface")  # Title
        title.setAlignment(Qt.AlignCenter)  # Center
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Pacing modes selection
        mode_label = QLabel("Select Pacing Mode:")  # Label
        self.mode_combo = QComboBox()  # Combo box
        self.mode_combo.addItems(["AOO", "VOO", "AAI", "VVI"])  # Add pacing modes

        # Programmable parameters display
        params_label = QLabel("Programmable Parameters:")  # Label for parameters
        params_label.setStyleSheet("font-weight: bold;")
        self.params_widget = QWidget()  # Label for parameters
        params_layout = QHBoxLayout()
        params_layout.addWidget(self.params_stacked_widget)
        self.params_widget.setLayout(params_layout)


        # bottom bar
        bottom_bar = QHBoxLayout()

        # Communication status
        comm_status_box = QVBoxLayout()
        comm_status_label = QLabel("Communication Status:")  # Label for communication status
        comm_status_label.setStyleSheet("font-weight: bold;")  # Bold text
        self.comm_status = QLabel("Not Connected")  # Placeholder status
        self.comm_status.setStyleSheet("color: red;")  # Red
        comm_status_box.addWidget(comm_status_label)  # Add communication status label
        comm_status_box.addWidget(self.comm_status)  # Add communication status
        bottom_bar.addLayout(comm_status_box)

        # Device identification status
        device_status_box = QVBoxLayout()
        device_status_label = QLabel("Device Status:")  # Label for device status
        device_status_label.setStyleSheet("font-weight: bold;")  # Bold text
        self.device_status = QLabel("No Device Detected")  # Placeholder status
        self.device_status.setStyleSheet("color: red;")  # Red
        device_status_box.addWidget(device_status_label)  # Add device status label
        device_status_box.addWidget(self.device_status)  # Add device status placeholder
        bottom_bar.addLayout(device_status_box)

        # Sign Out Button
        sign_out_button = QPushButton("Sign Out")
        sign_out_button.clicked.connect(self.dcm.sign_out)
        bottom_bar.addWidget(sign_out_button)

        # Assemble main layout
        self.layout.addWidget(title)  # Title
        self.layout.addWidget(mode_label)  # Add pacing mode label
        self.layout.addWidget(self.mode_combo)  # Add pacing mode
        self.layout.addWidget(params_label)  # Add parameters label
        self.layout.addWidget(self.params_widget)  # Add parameters label
        self.layout.addLayout(bottom_bar)

        self.mode_combo.currentTextChanged.connect(self.update_parameters)

    def update_parameters(self):
        selected_mode = self.mode_combo.currentText()
        # Find the index of the selected mode in the combo box
        index = self.mode_combo.findText(selected_mode)

        if index != -1:
            self.params_stacked_widget.setCurrentIndex(index)