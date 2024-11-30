from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QStackedWidget, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MainPage(QWidget):
    def __init__(self, dcm):
        super().__init__()

        self.dcm = dcm
        self.setup_layout()
        self.setLayout(self.layout)

    def setup_layout(self):
        """Sets up the main interface layout with labels, mode selection, and status indicators."""
        self.layout = QVBoxLayout()

        top_bar = QHBoxLayout()

        change_ui = QPushButton("Change UI")
        change_ui.clicked.connect(self.dcm.change_theme)

        title = QLabel("Pacemaker Control Monitor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        sign_out_button = QPushButton("Sign Out")
        sign_out_button.clicked.connect(self.sign_out)

        top_bar.addStretch()
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(change_ui)
        top_bar.addWidget(sign_out_button)


        # Parameter display

        data_bar = QHBoxLayout()

        self.mode_tabs = QTabWidget()
        for mode in self.dcm.pacemaker_modes:
            self.mode_tabs.addTab(self.dcm.pacemaker_modes[mode], mode)

        data_bar.addWidget(self.mode_tabs, 2)
        data_bar.addWidget(self.dcm.graph, 3)

        # Assemble layout
        self.layout.addLayout(top_bar)
        self.layout.addLayout(data_bar)
        self.setup_bottom_bar()

    def setup_bottom_bar(self):
        """Sets up the bottom bar layout with communication and device status."""
        bottom_bar = QHBoxLayout()

        data_box = QLabel(f"Serial ID: {self.dcm.pacemaker_serial} | Fortron v1.2 | McMaster University")

        # Communication status
        comm_status_box = QVBoxLayout()
        comm_status_label = QLabel("Communication Status:")
        comm_status_label.setStyleSheet("font-weight: bold;")
        self.comm_status = QLabel("No Data Transfer")
        self.comm_status.setStyleSheet("color: grey;")
        comm_status_box.addWidget(comm_status_label)
        comm_status_box.addWidget(self.comm_status)

        # Device identification status
        device_status_box = QVBoxLayout()
        device_status_label = QLabel("Device Status:")
        device_status_label.setStyleSheet("font-weight: bold;")
        self.device_status = QLabel("No Device Detected")
        self.device_status.setStyleSheet("color: red;")
        device_status_box.addWidget(device_status_label)
        device_status_box.addWidget(self.device_status)

        bottom_bar.addLayout(device_status_box)
        bottom_bar.addStretch()
        bottom_bar.addWidget(data_box)
        bottom_bar.addStretch()
        bottom_bar.addLayout(comm_status_box)
        self.layout.addLayout(bottom_bar)

    def sign_out(self):
        """Log out current user and return to the login page."""
        self.dcm.graph.reset_live_plot()
        self.dcm.graph.tabs.setCurrentIndex(0)
        self.mode_tabs.setCurrentIndex(0)
        self.dcm.page = 0
        self.dcm.run_gui()
