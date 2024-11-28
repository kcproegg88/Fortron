from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QVBoxLayout, QWidget, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        self.setCentralWidget(self.scroll_area)

        # Add some widgets to the scroll area
        for i in range(10):
            btn = QPushButton(f"Button {i}")
            self.scroll_area_layout.addWidget(btn)

        # Add a clear button to clear the layout
        clear_button = QPushButton("Clear Layout")
        clear_button.clicked.connect(self.clear_layout)
        self.scroll_area_layout.addWidget(clear_button)

    def clear_layout(self):
        clear_scroll_area_layout(self.scroll_area_layout)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
