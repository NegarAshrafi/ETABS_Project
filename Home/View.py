from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QMainWindow
from PyQt6 import *
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QCursor, QFont
import pyqtgraph as pg


class UI(QMainWindow):

    def __init__(self, filepath=None):

        super().__init__()

        self.show()
        self.name = filepath
        self.setGeometry(200, 200, 600, 300)
        self.setWindowTitle("Negar`s ETABS API")

        # main layout
        main_vbox = QVBoxLayout()
        self.setLayout(main_vbox)

        # 1st row
        hbox = QHBoxLayout()
        
        headerlabel = QLabel('Test Project \n\n by Negar Ashrafi')
        headerlabel.setFont(QFont('Arial', 12))
        # headerlabel.setStyleSheet(u"background: lightgray")
        headerlabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        headerlabel.setMaximumSize(120, 100)
        headerlabel.setMinimumSize(100, 80)
        hbox.addWidget(headerlabel)
        main_vbox.addLayout(hbox)

        # 2nd row
        hbox = QHBoxLayout()

        prelabel = QLabel('Previousely Connected to: ')
        prelabel.setMaximumWidth(150)
        prelabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(prelabel)
        # prelabel.setStyleSheet(u"background: lightgray")

        self.preetabs = QLabel('Previousely Connected to.......... ')
        hbox.addWidget(self.preetabs)
        # self.preetabs.setStyleSheet(u"background: lightgray")
        main_vbox.addLayout(hbox)

        # 3rd row
        hbox = QHBoxLayout()

        self.connect_btn = QPushButton('Connect to Etabs')
        self.connect_btn.setMaximumWidth(100)
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        hbox.addWidget(self.connect_btn)
        hbox.addSpacing(1)
        
        self.statuslabel = QLabel('Status Label')
        hbox.addWidget(self.statuslabel)
        main_vbox.addLayout(hbox)

        # empty room
        hbox = QHBoxLayout()
        hbox.addStretch(3)
        main_vbox.addLayout(hbox)

        # 4th row
        hbox = QHBoxLayout()

        self.driftbtn = QPushButton('Drift Control')
        hbox.addWidget(self.driftbtn)
        self.driftbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        hbox.addStretch(1)
        main_vbox.addLayout(hbox)

        # 5th row
        hbox = QHBoxLayout()

        self.prechecklbl = QLabel('Previously Checked as: ')
        self.prechecklbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.prechecklbl.setMaximumWidth(120)
        hbox.addWidget(self.prechecklbl)
        # self.prechecklbl.setStyleSheet(u"background: lightgray")

        self.preres = QLabel('Result ')

        hbox.addWidget(self.preres)
        # self.preres.setStyleSheet(u"background: lightgray")
        main_vbox.addLayout(hbox)

        # 6th row
        hbox = QHBoxLayout()
        self.clsbtn = QPushButton('Close', self)
        self.clsbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clsbtn.clicked.connect(self.close)
        hbox.addWidget(self.clsbtn)
        hbox.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_vbox.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(main_vbox)
        self.setCentralWidget(widget)
        
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
