from datetime import datetime
print("Starting:", datetime.now())
import sys
print("After sys:", datetime.now())
from PySide6.QtWidgets import QApplication
print("After PySide:", datetime.now())
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
print("After MainWindow import:", datetime.now())
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

ICON_PATH = BASE_DIR / "assets" / "pac_metrics.ico"

app = QApplication(sys.argv)
print("After QApplication:", datetime.now())

app.setWindowIcon(
    QIcon(str(ICON_PATH))
)

window = MainWindow()
print("After MainWindow creation:", datetime.now())

window.show()
print("After show:", datetime.now())

sys.exit(app.exec())