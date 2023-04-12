import path
import Home.Controller as Home
from PyQt6.QtWidgets import QApplication
import sys


path
if __name__ == '__main__':

    app = QApplication(sys.argv)
    drift = Home.ETABS()
    sys.exit(app.exec())
