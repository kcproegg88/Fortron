from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QSlider
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

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
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.dcm.save_parameters)
        self.save_button.setStyleSheet("background-color: #5cb85c; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")
        self.load_data_button = QPushButton("Load Egram Data")
        self.load_data_button.setStyleSheet("background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")
        self.send_data_button = QPushButton("Send to Pacemaker")
        self.send_data_button.setStyleSheet("background-color: #d9534f; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")

        # Adding buttons to the layout
        parameter_buttons_layout.addWidget(self.save_button)
        parameter_buttons_layout.addWidget(self.load_data_button)
        parameter_buttons_layout.addWidget(self.send_data_button)
        self.layout.addStretch()
        self.layout.addLayout(parameter_buttons_layout)

        # # Display logo
        # logo_label = QLabel()
        # logo_label.setPixmap(QPixmap("grid.png"))
        # self.layout.addWidget(logo_label, 1, 3, len(self.parameters), 1)

    def update_parameters(self):
        """Update parameter sliders and labels with user data."""
        for i in range(len(self.parameters)):
            self.parameters[i].update_value_label(self.dcm.user_data[self.name][i])

    def send_values(self):
        """Gather current parameter values for further processing"""
        return [parameter.value for parameter in self.parameters]
