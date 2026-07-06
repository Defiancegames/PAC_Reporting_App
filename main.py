import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from datetime import datetime

print("Starting:", datetime.now())

import sys
print("After sys:", datetime.now())

from PySide6.QtWidgets import QApplication
print("After PySide:", datetime.now())

from ui.main_window import MainWindow
print("After MainWindow import:", datetime.now())

app = QApplication(sys.argv)
print("After QApplication:", datetime.now())

window = MainWindow()
print("After MainWindow creation:", datetime.now())

window.show()
print("After show:", datetime.now())

sys.exit(app.exec())