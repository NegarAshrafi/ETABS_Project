from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout,\
                            QPushButton, QMainWindow
from PyQt6 import *
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QCursor
import pyqtgraph as pg
from pathlib import Path


# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class UI(QMainWindow):

    def __init__(self, filepath=None):
        
        super().__init__()
        # self.setupUi(self)
        self.show()
        self.name = filepath
        self.setGeometry(200, 200, 700, 400 )

        self.setWindowTitle("My App")

        self.layout = QVBoxLayout()
        # self.setLayout(self.layout)

        self.head = QHBoxLayout()
        self.main = QGridLayout()
        self.foot = QHBoxLayout()

        # self.head.addStretch(2)
        self.head.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(self.head)
        self.layout.addLayout(self.main)
        self.layout.addLayout(self.foot)

        self.headerlabel = QLabel('Test Project \n by Negar Ashrafi', self)
        self.headerlabel.setStyleSheet(u"background: lightgray")
        self.head.addWidget(self.headerlabel)

        self.frstlb = QHBoxLayout()
        self.main.addLayout(self.frstlb, 0,0)

        self.prelabel = QLabel('Previousely Connected to: ', self)
        self.main.addWidget(self.prelabel, 0,0)
        self.prelabel.setStyleSheet(u"background: lightgray")

        self.preetabs = QLabel('Previousely Connected to.......... ', self)
        self.main.addWidget(self.preetabs, 0,1,1,2)
        self.preetabs.setStyleSheet(u"background: lightgray")

        self.prebtnlayout = QHBoxLayout()
        self.main.addLayout(self.prebtnlayout, 1, 0)

        self.statuslayout = QHBoxLayout()
        self.main.addLayout(self.statuslayout, 1, 1)

        self.connect_btn = QPushButton('Connect to Etabs', self)
        self.prebtnlayout.addWidget(self.connect_btn)
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.statuslabel = QLabel('Status Label')
        self.prebtnlayout.addWidget(self.statuslabel)

        self.driftbtnlayout = QHBoxLayout()
        self.main.addLayout(self.driftbtnlayout, 2, 0)
        self.driftbtnlayout.addStretch(3)

        self.driftbtn = QPushButton('Drift Control')
        self.driftbtnlayout.addWidget(self.driftbtn)
        self.driftbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.prechecklayout = QHBoxLayout()
        self.main.addLayout(self.prechecklayout, 3 ,0)

        self.prechecklbl = QLabel('Previously checked as: ')
        self.prechecklayout.addWidget(self.prechecklbl)
        self.prechecklbl.setStyleSheet(u"background: lightgray")

        self.preres = QLabel('Result ')
        self.prechecklayout.addWidget(self.preres)
        self.preres.setStyleSheet(u"background: lightgray")

        self.clsbtn = QPushButton('Close', self)
        self.foot.addWidget(self.clsbtn, 3)
        self.clsbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clsbtn.clicked.connect(self.close)

        widget = QWidget()
        widget.setLayout(self.layout)
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

        else: return False
