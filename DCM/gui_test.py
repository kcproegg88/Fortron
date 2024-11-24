from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel


class TabbedWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        # Create tabs
        self.addTab(self.create_tab("Tab 1 Content"), "Tab 1")
        self.addTab(self.create_tab("Tab 2 Content"), "Tab 2")
        self.addTab(self.create_tab("Tab 3 Content"), "Tab 3")

        # Set window title
        self.setWindowTitle("QTabWidget Example")

    def create_tab(self, text):
        """Create a tab with a QLabel."""
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab


if __name__ == "__main__":
    app = QApplication([])
    window = TabbedWindow()
    window.resize(400, 300)
    window.show()
    app.exec()
