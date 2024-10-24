from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton, QSlider
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator


class PaceMakerParameter(QWidget):
    def __init__(self, param_list):
        super().__init__()
        print(param_list)
        self.name = param_list[0]
        self.value = (param_list[2]-param_list[1])//2 + param_list[1]
        self.decimal = param_list[3]
        self.name_label = QLabel(f"{self.name}: {self.value/self.decimal}")
        self.inputBox = QSlider(Qt.Horizontal)
        self.inputBox.setMinimum(param_list[1])
        self.inputBox.setMaximum(param_list[2])
        self.inputBox.setValue(self.value)
        self.inputBox.valueChanged.connect(self.update_value_label)

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.inputBox)
        self.name_label.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")
        self.setLayout(layout)

    def update_value_label(self, value):
        self.value = value
        self.name_label.setText(f"{self.name}: {self.value/self.decimal}")


class PaceMakerMode(QWidget):
    def __init__(self, mode_name, parameters):
        super().__init__()

        self.mode_name = QLabel(mode_name)
        self.mode_name.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")

        self.parameters = [PaceMakerParameter(param_list) for param_list in parameters]
        print("here")
        self.layout = QGridLayout()
        self.layout.addWidget(self.mode_name, 0, 0, 1, 4)
        self.setLayout(self.layout)
        self.add_parameters()

    def add_parameters(self):
        for i in range(len(self.parameters)):
            self.layout.addWidget(self.parameters[i], i+1, 0)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.addWidget(QLabel("Hello"), 1,1, len(self.parameters),1)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_values)
        # self.load_data_button = QPushButton("")
        self.layout.addWidget(self.save_button, len(self.parameters)+2, 0)

    def save_values(self):
        print(*[i.value for i in self.parameters], sep=" ")