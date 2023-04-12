from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QCursor
from pathlib import Path


class WellcomeWindow(QWidget):

    def __init__(self, etabs):
        super().__init__()

        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle("ETABS API")

        # main layout
        main_vbox = QVBoxLayout()
        self.setLayout(main_vbox)

        # 1st row
        hbox = QHBoxLayout()
        win_lable = QLabel('Wellcom to ETABS API App')
        hbox.addWidget(win_lable)
        win_lable.setAlignment(Qt.AlignmentFlag.AlignBottom)
        main_vbox.addLayout(hbox)

        # 2nd row
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        self.new_file_btn = QPushButton('Add ETABS Proj.')
        self.new_file_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.new_file_btn.setMinimumWidth(120)
        self.new_file_btn.setMaximumWidth(180)
        vbox.addWidget(self.new_file_btn)
        vbox.setAlignment(Qt.AlignmentFlag.AlignBottom)
        hbox.addLayout(vbox)
        main_vbox.addLayout(hbox)

        # 3rd row
        hbox = QHBoxLayout()
        self.connect_btn = QPushButton('Connect to Active File')
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.connect_btn.setMinimumWidth(120)
        self.connect_btn.setMaximumWidth(180)
        hbox.addWidget(self.connect_btn)
        main_vbox.addLayout(hbox)

        # 4th row
        hbox = QHBoxLayout()
        self.status_lbl = QLabel('Connected to: ...')
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(self.status_lbl)
        main_vbox.addLayout(hbox)

        # 5th row
        hbox = QHBoxLayout()
        self.run_btn = QPushButton('Run')
        self.run_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_btn.setFixedSize(80, 50)
        self.run_btn.setEnabled(False)
        hbox.addWidget(self.run_btn)
        main_vbox.addLayout(hbox)

        # 6th row
        hbox = QHBoxLayout()
        self.run_status = QLabel('Run Status...')
        self.run_status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        hbox.addWidget(self.run_status)
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

            if self.name == None:
                return False
            else:
                print(f'in open dialog of view self.name is : {self.name}')
                return self.name

        else:
            return False
