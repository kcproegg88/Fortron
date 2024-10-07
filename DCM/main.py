from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys
app = QApplication([])
window = QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60, 15)
window.show()
sys.exit(app.exec())