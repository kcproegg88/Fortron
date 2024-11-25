from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QSlider
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
        self.inputBox.setValue(self.value)
        self.name_label.setText(f"{self.name}: {self.value / self.decimal}")


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
        self.add_parameters()

    def add_parameters(self):
        """Add parameter widgets to the layout"""
        for i in range(len(self.parameters)):
            self.layout.addWidget(self.parameters[i])

        # Save, Load, and Send buttons with improved styles
        parameter_buttons_layout = QHBoxLayout()
        save_mode_button = QPushButton("Save Mode")
        save_mode_button.clicked.connect(self.dcm.save_mode)
        save_mode_button.setStyleSheet("background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        reset_parameters_button = QPushButton("Reset Parameters")
        reset_parameters_button.clicked.connect(self.reset_parameters)
        reset_parameters_button.setStyleSheet("background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        send_data_button = QPushButton("Send to Pacemaker")
        send_data_button.clicked.connect(self.transmit_mode)
        send_data_button.setStyleSheet("background-color: #d9534f; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        # Adding buttons to the layout
        parameter_buttons_layout.addWidget(save_mode_button)
        parameter_buttons_layout.addWidget(reset_parameters_button)
        parameter_buttons_layout.addWidget(send_data_button)
        self.layout.addStretch()
        self.layout.addLayout(parameter_buttons_layout)

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
        result = serial_comm(self.dcm.check_port_connection(), 22, 34, {i.name: i.value for i in self.parameters}, index+1)
        print(result)

    def send_values(self):
        """Gather current parameter values for further processing"""
        return [parameter.value for parameter in self.parameters]
