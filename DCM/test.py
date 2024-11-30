import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Switcher")

        # Main layout
        layout = QVBoxLayout()

        # Buttons to change themes
        light_button = QPushButton("Light Theme")
        light_button.clicked.connect(lambda: self.change_theme("light.qss"))

        dark_button = QPushButton("Dark Theme")
        dark_button.clicked.connect(lambda: self.change_theme("dark.qss"))

        blue_button = QPushButton("Blue Theme")
        blue_button.clicked.connect(lambda: self.change_theme("blue.qss"))

        # Add buttons to layout
        layout.addWidget(light_button)
        layout.addWidget(dark_button)
        layout.addWidget(blue_button)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def change_theme(self, theme_file):
        """Load the selected QSS file and apply the stylesheet."""
        try:
            with open(theme_file, "r") as file:
                qss = file.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Theme file {theme_file} not found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
