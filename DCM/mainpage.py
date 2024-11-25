from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QStackedWidget, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import styling  # Add this import



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

        title = QLabel("DCM Main Interface")
        title.setAlignment(Qt.AlignCenter)

        top_bar.addWidget(title)

        # Parameter display

        data_bar = QHBoxLayout()

        self.mode_tabs = QTabWidget()
        for mode in self.dcm.pacemaker_modes:
            self.mode_tabs.addTab(self.dcm.pacemaker_modes[mode], mode)

        data_bar.addWidget(self.mode_tabs, 1)
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("grid.png"))
        data_bar.addWidget(logo_label, 1)

        # Assemble layout
        self.layout.addLayout(top_bar)
        self.layout.addLayout(data_bar)
        self.setup_setting_bar()
        self.setup_bottom_bar()

    def setup_setting_bar(self):
        setting_bar = QHBoxLayout()
        
        save_all_button = QPushButton("Save All Modes")
        reset_all_button = QPushButton("Reset All Modes")
        change_ui = QPushButton("Change UI")
        change_ui.clicked.connect(self.dcm.change_theme)
        for button in [save_all_button, reset_all_button, change_ui]:
            setting_bar.addWidget(button)
        self.layout.addLayout(setting_bar)

    def setup_bottom_bar(self):
        """Sets up the bottom bar layout with communication and device status."""
        bottom_bar = QHBoxLayout()

        # Communication status
        comm_status_box = QVBoxLayout()
        comm_status_label = QLabel("Communication Status:")
        self.comm_status = QLabel("Not Connected")
        comm_status_box.addWidget(comm_status_label)
        comm_status_box.addWidget(self.comm_status)
        bottom_bar.addLayout(comm_status_box)

        # Device identification status
        device_status_box = QVBoxLayout()
        device_status_label = QLabel("Device Status:")
        self.device_status = QLabel("No Device Detected")
        device_status_box.addWidget(device_status_label)
        device_status_box.addWidget(self.device_status)
        bottom_bar.addLayout(device_status_box)

        # Sign Out Button
        sign_out_button = QPushButton("Sign Out")
        sign_out_button.clicked.connect(self.sign_out)
        bottom_bar.addWidget(sign_out_button)
        self.layout.addLayout(bottom_bar)

    def sign_out(self):
        """Log out current user and return to the login page."""
        self.dcm.page = 0
        self.dcm.run_gui()
