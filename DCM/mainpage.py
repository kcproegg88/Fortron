from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QStackedWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from parameter_display import PaceMakerMode


class MainPage(QWidget):
    def __init__(self, dcm):
        super().__init__()

        self.dcm = dcm
        self.params_stacked_widget = QStackedWidget()  # Holds mode-specific parameter interfaces

        # Initialize modes with their respective parameters
        self.init_modes()

        # Main layout setup
        self.layout = QVBoxLayout()
        self.setup_layout()
        self.setLayout(self.layout)
        # Connect mode selection combo box to update parameters
        self.mode_combo.currentTextChanged.connect(self.update_mode_selection)

    def init_modes(self):
        """Creates and adds parameter widgets for each pacing mode."""
        modes_params = {
            "AOO": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Atrial amplitude", 5, 32, 10], ["Atrial pulse width", 5, 190, 100]],
            "VOO": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Ventricular amplitude", 5, 32, 10], ["Ventricular pulse width", 5, 190, 100]],
            "AAI": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Atrial amplitude", 5, 32, 10], ["Atrial pulse width", 5, 190, 100],
                    ["Atrial sensitivity", 25, 1000, 100], ["ARP", 150, 500, 1], ["PVARP", 150, 500, 1]],
            "VVI": [["Lower rate limit", 30, 175, 1], ["Upper rate limit", 50, 175, 1],
                    ["Ventricular amplitude", 5, 32, 10], ["Ventricular pulse width", 5, 190, 100],
                    ["Ventricular sensitivity", 25, 1000, 100], ["VRP", 150, 500, 1],
                    ["Hysteresis interval", 200, 500, 1], ["Low rate interval", 343, 2000, 1]]}

        for mode, params in modes_params.items():
            mode_widget = PaceMakerMode(mode, self.dcm, params)
            self.params_stacked_widget.addWidget(mode_widget)
            self.dcm.pacemaker_modes[mode] = mode_widget

    def setup_layout(self):
        """Sets up the main interface layout with labels, mode selection, and status indicators."""
        # Title
        title = QLabel("DCM Main Interface")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Mode selection
        mode_label = QLabel("Select Pacing Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["AOO", "VOO", "AAI", "VVI"])

        # Parameter display
        params_label = QLabel("Programmable Parameters:")
        params_label.setStyleSheet("font-weight: bold;")
        self.params_widget = QWidget()
        params_layout = QHBoxLayout()
        params_layout.addWidget(self.params_stacked_widget)
        self.params_widget.setLayout(params_layout)

        # Bottom bar with status and sign-out button
        bottom_bar = self.setup_bottom_bar()

        # Assemble layout
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
        sign_out_button.clicked.connect(self.dcm.sign_out)
        bottom_bar.addWidget(sign_out_button)

        return bottom_bar

    def update_mode_selection(self):
        """Switches displayed parameters based on selected pacing mode."""
        selected_mode = self.mode_combo.currentText()
        index = self.mode_combo.findText(selected_mode)
        if index != -1:
            self.params_stacked_widget.setCurrentIndex(index)
