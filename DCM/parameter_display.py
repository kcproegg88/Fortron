from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QSlider, QScrollArea
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from serial_coms import serial_comm


class PaceMakerParameter(QWidget):
    def __init__(self, param_list, value):
        super().__init__()

        # Initialize the parameter's name, value, and decimal scaling
        self.name = param_list[0]
        self.value = value
        self.decimal = param_list[3]

        # Create a label to display the parameter's name and current value
        self.name_label = QLabel(f"{self.name}: {self.value / self.decimal}")
        self.name_label.setStyleSheet("color: black; font-size: 14px; padding: 5px;")  # Add padding
        self.name_label.setWordWrap(True)  # Enable wrapping for long text

        # Set up a slider for user input on the parameter value
        self.inputBox = QSlider(Qt.Horizontal)
        self.inputBox.setMinimum(param_list[1])
        self.inputBox.setMaximum(param_list[2])
        self.inputBox.setValue(self.value)
        self.inputBox.valueChanged.connect(self.update_value_label)

        # Layout configuration for the parameter display
        layout = QHBoxLayout()
        layout.addWidget(self.name_label, stretch=2)  # Expand label area
        layout.addWidget(self.inputBox, stretch=3)  # Allow the slider to occupy more space
        self.setLayout(layout)

    def update_value_label(self, value):
        """Update the displayed value when the slider changes"""
        self.value = value
        if self.name == "Lower rate limit" or self.name == "Hysteresis":
            if 30 <= self.value <= 50 or 90 <= self.value <= 175:
                self.value -= self.value % 5
        elif self.name == "Upper rate limit" or self.name == "Maximum Sensor Rate":
            self.value -= self.value % 5
        elif self.name == "Rate Smoothing":
            self.value -= self.value % 3
            if self.value > 21:
                self.value = 25

        # self.inputBox.setValue(self.value)
        self.name_label.setText(f"{self.name}: {self.value / self.decimal}")
        if self.name in ["Lower rate limit", "Upper rate limit", "Maximum Sensor Rate", "Hysteresis"]:
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)} ppm")
        elif self.name in ["Atrial amplitude", "Ventricular amplitude"] :
            self.name_label.setText(f"{self.name}: {self.value / self.decimal} V")
        elif self.name in ["Atrial pulse width", "Ventricular pulse width", "ARP", "VRP", "PVARP"]:
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)} ms")
        elif self.name in ["Atrial Sensitivity", "Ventricular Sensitivity"]:
            self.name_label.setText(f"{self.name}: {self.value / self.decimal} mV")
        elif self.name == "Rate Smoothing":
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)} %")
        elif self.name == "Reaction Time":
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)} s")
        elif self.name == "Response Factor":
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)}")
        elif self.name == "Recovery Time":
            self.name_label.setText(f"{self.name}: {int(self.value / self.decimal)} min")

        if self.name == "Hysteresis" and self.value < 30:
            self.name_label.setText(f"{self.name}: OFF")
        elif self.name == "Rate Smoothing" and self.value == 0:
            self.name_label.setText(f"{self.name}: OFF")
        elif self.name == "Activity Threshold":
            self.name_label.setText(f"{self.name}: {(["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"])[self.value]}")


class PaceMakerMode(QWidget):
    def __init__(self, mode_name, dcm, parameters):
        super().__init__()
        self.dcm = dcm
        self.name = mode_name

        # Create a label for the mode name
        self.mode_name = QLabel(self.name)
        self.mode_name.setStyleSheet("color: black; font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        # Initialize parameters for this mode using PaceMakerParameter instances
        self.parameters = [PaceMakerParameter(parameters[i], self.dcm.default_data[mode_name][i]) for i in range(len(parameters))]
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mode_name)
        self.setLayout(self.layout)
        self.init_layout()

    def init_layout(self):
        self.add_parameters()
        # Save, Load, and Send buttons with improved styles
        parameter_buttons_layout = QHBoxLayout()
        save_mode_button = QPushButton("Save Mode")
        save_mode_button.clicked.connect(self.dcm.save_mode)
        save_mode_button.setStyleSheet(
            "background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        reset_parameters_button = QPushButton("Reset Parameters")
        reset_parameters_button.clicked.connect(self.reset_parameters)
        reset_parameters_button.setStyleSheet(
            "background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        send_data_button = QPushButton("Send to Pacemaker")
        send_data_button.clicked.connect(self.transmit_mode)
        send_data_button.setStyleSheet(
            "background-color: #d9534f; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        # Adding buttons to the layout
        parameter_buttons_layout.addWidget(save_mode_button)
        parameter_buttons_layout.addWidget(reset_parameters_button)
        parameter_buttons_layout.addWidget(send_data_button)
        self.layout.addLayout(parameter_buttons_layout)

    def add_parameters(self):
        """Add parameter widgets to the layout"""
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout()
        for i in range(len(self.parameters)):
            scroll_area_layout.addWidget(self.parameters[i])
        scroll_area_layout.addStretch()
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

    def update_parameters(self):
        """Update parameter sliders and labels with user data."""
        for i in range(len(self.parameters)):
            self.parameters[i].update_value_label(self.dcm.user_data[self.name][i])

    def reset_parameters(self):
        for i in range(len(self.parameters)):
            self.parameters[i].update_value_label(self.dcm.default_data[self.name][i])

    def transmit_mode(self):
        print({i.name: i.value for i in self.parameters})
        index = list(self.dcm.pacemaker_modes.keys()).index(self.name)
        result = 0
        try:
            serial_comm(self.dcm.check_port_connection(), 22, 85, {i.name: i.value for i in self.parameters}, index + 1)
            result = serial_comm(self.dcm.check_port_connection(), 22, 34, {i.name: i.value for i in self.parameters}, index + 1)
        except Exception as e:
            print(e)
        print(result)

    def send_values(self):
        """Gather current parameter values for further processing"""
        return [parameter.value for parameter in self.parameters]
