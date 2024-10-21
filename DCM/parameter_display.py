from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt


class PaceMakerParameter(QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")


class PaceMakerMode(QWidget):
    def __init__(self, mode_name, parameters):
        super().__init__()
        self.mode_name = QLabel(mode_name)
        self.mode_name.setStyleSheet("color: rgb(0, 0, 0);\nborder: 1px solid black;\n")

        self.parameters = [PaceMakerParameter(name) for name in parameters]
        self.layout = QGridLayout()
        self.layout.addWidget(self.mode_name, 0, 0, 2, 2)
        self.setLayout(self.layout)
        self.add_parameters()

    def add_parameters(self):
        for i in range(len(self.parameters)):
            self.layout.addWidget(self.parameters[i], i+1, 0)