from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QStackedWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt


class MainPage(QWidget):
    def __init__(self, dcm):
        super().__init__()

        self.dcm = dcm
        self.params_stacked_widget = QStackedWidget()  # Holds mode-specific parameter interfaces

        # Initialize modes with their respective parameters
        for mode in self.dcm.pacemaker_modes:
            self.params_stacked_widget.addWidget(self.dcm.pacemaker_modes[mode])

        # Main layout setup
        self.setup_layout()
        self.setLayout(self.layout)

    def setup_layout(self):
        """Sets up the main interface layout with labels, mode selection, and status indicators."""
        # Title
        title = QLabel("DCM Main Interface")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Mode selection
        combo_style = """
        QComboBox {
            background-color: #f0f0f0;
            border: 1px solid #5c5c5c;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: #333333;
        }

        QComboBox:hover {
            background-color: #e6e6e6;
        }

        QComboBox::drop-down {
            border-left: 1px solid #5c5c5c;
            background-color: #dcdcdc;
            width: 20px;
        }

        QComboBox::down-arrow {
            image: url(down_arrow.png); /* Replace with your custom arrow image */
            width: 10px;
            height: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #5c5c5c;
            border-radius: 5px;
            padding: 2px;
            selection-background-color: #0078d7;
            selection-color: white;
        }
        """
        mode_label = QLabel("Select Pacing Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(self.dcm.pacemaker_modes.keys())
        self.mode_combo.setStyleSheet(combo_style)
        self.mode_combo.currentTextChanged.connect(self.update_mode_selection)
        

        # Parameter display
        params_label = QLabel("Programmable Parameters:")
        params_label.setStyleSheet("font-weight: bold;")
        self.params_widget = QWidget()
        params_layout = QHBoxLayout()
        params_layout.addWidget(self.params_stacked_widget)
        self.params_widget.setLayout(params_layout)

        # Interface Bare with Save Load and Send button

        # Bottom bar with status and sign-out button
        bottom_bar = self.setup_bottom_bar()

        # Assemble layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(title)
        self.layout.addWidget(mode_label)
        self.layout.addWidget(self.mode_combo)
        self.layout.addWidget(params_label)
        self.layout.addWidget(self.params_widget)
        self.layout.addLayout(bottom_bar)

    def setup_bottom_bar(self):
        """Sets up the bottom bar layout with communication and device status."""
        bottom_bar = QHBoxLayout()

        # Communication status
        comm_status_box = QVBoxLayout()
        comm_status_label = QLabel("Communication Status:")
        comm_status_label.setStyleSheet("font-weight: bold;")
        self.comm_status = QLabel("Not Connected")
        self.comm_status.setStyleSheet("color: red;")
        comm_status_box.addWidget(comm_status_label)
        comm_status_box.addWidget(self.comm_status)
        bottom_bar.addLayout(comm_status_box)

        # Device identification status
        device_status_box = QVBoxLayout()
        device_status_label = QLabel("Device Status:")
        device_status_label.setStyleSheet("font-weight: bold;")
        self.device_status = QLabel("No Device Detected")
        self.device_status.setStyleSheet("color: red;")
        device_status_box.addWidget(device_status_label)
        device_status_box.addWidget(self.device_status)
        bottom_bar.addLayout(device_status_box)

        # Sign Out Button
        sign_out_button = QPushButton("Sign Out")
        sign_out_button.setStyleSheet("background-color: #0275d8; color: white; padding: 5px; font-size: 14px; border-radius: 5px;")
        sign_out_button.clicked.connect(self.sign_out)
        bottom_bar.addWidget(sign_out_button)
        return bottom_bar

    def update_mode_selection(self):
        """Switches displayed parameters based on selected pacing mode."""
        index = self.mode_combo.findText(self.mode_combo.currentText())
        self.params_stacked_widget.setCurrentIndex(index)

    def sign_out(self):
        """Log out current user and return to the login page."""
        self.dcm.page = 0
        self.dcm.run_gui()
