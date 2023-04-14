from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QStyle, QMessageBox
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QCursor, QFont, QIcon
from pathlib import Path


class WellcomeWindow(QWidget):

    def __init__(self, etabs):
        super().__init__()

        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle("ETABS API")
        self.setWindowIcon(QIcon('ETABS_Project/utilities/ETABS1.png'))
        self.setStyleSheet("background-color: rgb(255,250,220); border:1px solid rgb(170, 230, 190); ")

        # main layout
        main_vbox = QVBoxLayout()
        self.setLayout(main_vbox)

        # 1st row
        hbox = QHBoxLayout()
        self.preetabs = QLabel('Pre')
        self.preetabs.setFont(QFont('Arial', 8))
        self.preetabs.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.preetabs.setFixedHeight(20)
        self.preetabs.setStyleSheet("background-color: lightblue;")
        hbox.addWidget(self.preetabs)
        main_vbox.addLayout(hbox)

        # 1st row
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox2 = QHBoxLayout()
        hbox.addStretch(2)
        hbox2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.new_file_btn = QPushButton('Open File')
        self.new_file_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.new_file_btn.setMinimumWidth(120)
        self.new_file_btn.setMaximumWidth(150)
        self.new_file_btn.setMinimumHeight(80)
        pixmapi = QStyle.StandardPixmap.SP_DialogOpenButton
        icon = self.style().standardIcon(pixmapi)
        self.new_file_btn.setIcon(icon)
        hbox2.addWidget(self.new_file_btn)
        hbox2.setAlignment(Qt.AlignmentFlag.AlignBottom)
        hbox.addLayout(hbox2)

        hbox2 = QHBoxLayout()
        self.connect_btn = QPushButton('Connect to\nActive File')
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.connect_btn.setMinimumWidth(120)
        self.connect_btn.setMaximumWidth(150)
        self.connect_btn.setMinimumHeight(80)
        pixmapi = QStyle.StandardPixmap.SP_BrowserReload
        icon = self.style().standardIcon(pixmapi)
        self.connect_btn.setIcon(icon)
        hbox2.addWidget(self.connect_btn)
        hbox2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox.addLayout(hbox2)
        hbox.addStretch(2)
        main_vbox.addLayout(hbox)

        # 2nd row
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.run_drift_btn = QPushButton('Check Drift')
        self.run_drift_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_drift_btn.setMinimumHeight(60)
        self.run_drift_btn.setMinimumWidth(90)
        self.run_drift_btn.setEnabled(False)
        pixmapi = QStyle.StandardPixmap.SP_MediaPlay
        icon = self.style().standardIcon(pixmapi)
        self.run_drift_btn.setIcon(icon)
        hbox2.addWidget(self.run_drift_btn)
        hbox2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addLayout(hbox2)
        main_vbox.addLayout(hbox)

        # 3rd row
        hbox = QHBoxLayout()
        self.etabs_path = QLabel('ETABS Path')
        self.etabs_path.setFont(QFont('Arial', 8))
        self.etabs_path.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.etabs_path.setMaximumHeight(20)
        hbox.addWidget(self.etabs_path)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.etabs_path.setStyleSheet(u"background: lightblue")
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.addLayout(hbox)

    @pyqtSlot()
    def open_dialog(self, last_path) -> str:
        """ open dialog browser and return file path """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("ETABS Model Files(*.edb);;ETABS Model Files(*.EDB)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setDirectory(last_path)

        if dialog.exec():

            filepathname = dialog.selectedFiles()
            self.name = Path(filepathname[0])

            if self.name is None:
                return False
            else:
                print(f'in open dialog of view self.name is : {self.name}')
                return self.name

        else:
            return False

    def active_file(self):

        self.msg_box = QMessageBox(self)
        self.msg_box.setWindowTitle("Warning")
        self.msg_box.setText("There is not any Active ETABS File")
        self.msg_box.Icon.Warning
        btn = self.msg_box.exec()

        if btn == QMessageBox.StandardButton.Retry:
            pass
