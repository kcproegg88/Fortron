from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QSlider
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout
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

        # Set up a slider for user input on the parameter value
        self.inputBox = QSlider(Qt.Horizontal)
        self.inputBox.setMinimum(param_list[1])
        self.inputBox.setMaximum(param_list[2])
        self.inputBox.setValue(self.value)
        self.inputBox.valueChanged.connect(self.update_value_label)

        # Layout configuration for the parameter display
        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.inputBox)
        self.name_label.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
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
        self.mode_name.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")

        # Initialize parameters for this mode using PaceMakerParameter instances
        self.parameters = [PaceMakerParameter(parameters[i], self.dcm.default_data[mode_name][i]) for i in
                           range(len(parameters))]
        self.layout = QGridLayout()
        self.layout.addWidget(self.mode_name, 0, 0, 1, 4)
        self.setLayout(self.layout)
        self.add_parameters()

    def add_parameters(self):
        """Add parameter widgets to the layout"""
        for i in range(len(self.parameters)):
            self.layout.addWidget(self.parameters[i], i + 1, 0)

        # Set stretch properties for better layout
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        # Additional UI elements like buttons and labels
        self.layout.addWidget(QLabel("Hello"), 1, 1, len(self.parameters), 1)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.dcm.save_parameters)
        self.load_data_button = QPushButton("Load Egram Data")
        self.send_data_button = QPushButton("Send to Pacemaker")

        # Adding buttons to the layout
        self.layout.addWidget(self.save_button, len(self.parameters) + 2, 0)
        self.layout.addWidget(self.load_data_button, len(self.parameters) + 2, 1)
        self.layout.addWidget(self.send_data_button, len(self.parameters) + 2, 3)

        # Display logo in the layout
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("grid.png"))
        self.layout.addWidget(logo_label, 1, 1, len(self.parameters), 2)

    def update_parameters(self):
        for i in range(len(self.parameters)):
            self.parameters[i].update_value_label(self.dcm.user_data[self.name][i])

    def send_values(self):
        """Gather current parameter values for further processing"""
        return [parameter.value for parameter in self.parameters]