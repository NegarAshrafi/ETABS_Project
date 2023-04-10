from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QRadioButton, QVBoxLayout, QHBoxLayout, QGridLayout, QListWidget,\
                            QPushButton, QMainWindow, QTableWidget, QAbstractItemView, QApplication
from PyQt6 import *
from PyQt6.QtCore import pyqtSlot, Qt, QRect
from PyQt6.QtGui import QCursor
import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtWidgets
# from pyqtgraph import GraphicsLayoutWidget
# import pyqtgraph.exporters
from pathlib import Path
# from PyQt6 import uic
import sys


# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

print('drift view')
# class WindowStructure(QWidget):
#     print('birahe')
#     def __init__(self) -> None:
#         super().__init__()

#     # def main_layout(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
        
#         self.head = QHBoxLayout()
#         self.main = QGridLayout()
#         self.foot = QHBoxLayout()

#         # self.head.addStretch(2)
#         self.head.setAlignment(Qt.AlignmentFlag.AlignHCenter)

#         self.layout.addLayout(self.head)
#         self.layout.addLayout(self.main)
#         self.layout.addLayout(self.foot)

#         self.prelabel = QLabel('Previousely Connected to: ', self)
#         self.main.addWidget(self.prelabel, 0,0)
#         self.prelabel.setStyleSheet(u"background: lightgray")

#     def btn (self, pos=QRect(700, 480, 100, 33),
#                   color=u"background: rgb(0, 85,255)"):
#         self.butt = QPushButton(self)
#         self.butt.setGeometry(pos)
#         self.butt.setStyleSheet(color)
#         return self.butt

# app = QApplication(sys.argv)
# class UI(QMainWindow):
#     print('class ui')
#     def __init__(self, filepath=None):
        
#         super().__init__()
#         # self.setupUi(self)
#         self.show()
#         self.name = filepath
#         self.setGeometry(200,200, 700, 400)

#         self.setWindowTitle("My App")

#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
        
#         self.head = QHBoxLayout()
#         self.main = QGridLayout()
#         self.foot = QHBoxLayout()

#         # self.head.addStretch(2)
#         self.head.setAlignment(Qt.AlignmentFlag.AlignHCenter)

#         self.layout.addLayout(self.head)
#         self.layout.addLayout(self.main)
#         self.layout.addLayout(self.foot)

#         self.headerlabel = QLabel('Test Project \n by Negar Ashrafi', self)
#         self.headerlabel.setStyleSheet(u"background: lightgray")
#         self.head.addWidget(self.headerlabel)

#         self.frstlb = QHBoxLayout()
#         self.main.addLayout(self.frstlb, 0,0)
        
#         self.prelabel = QLabel('Previousely Connected to: ', self)
#         self.main.addWidget(self.prelabel, 0,0)
#         self.prelabel.setStyleSheet(u"background: lightgray")
        
#         self.preetabs = QLabel('Previousely Connected to.......... ', self)
#         self.main.addWidget(self.preetabs, 0,1,1,2)
#         self.preetabs.setStyleSheet(u"background: lightgray")

#         self.prebtnlayout = QHBoxLayout()
#         self.main.addLayout(self.prebtnlayout, 1, 0)

#         self.statuslayout = QHBoxLayout()
#         self.main.addLayout(self.statuslayout, 1, 1)
        
#         self.connect_btn = QPushButton('Connect to Etabs', self)
#         self.prebtnlayout.addWidget(self.connect_btn)
#         self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

#         self.statuslabel = QLabel('Status Label')
#         self.prebtnlayout.addWidget(self.statuslabel)
        
#         self.driftbtnlayout = QHBoxLayout()
#         self.main.addLayout(self.driftbtnlayout, 2, 0)
#         self.driftbtnlayout.addStretch(3)

#         self.driftbtn = QPushButton('Drift Control')
#         self.driftbtnlayout.addWidget(self.driftbtn)
#         self.driftbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

#         self.prechecklayout = QHBoxLayout()
#         self.main.addLayout(self.prechecklayout, 3 ,0)

#         self.prechecklbl = QLabel('Previously checked as: ')
#         self.prechecklayout.addWidget(self.prechecklbl)
#         self.prechecklbl.setStyleSheet(u"background: lightgray")
        
#         self.preres = QLabel('Result ')
#         self.prechecklayout.addWidget(self.preres)
#         self.preres.setStyleSheet(u"background: lightgray")

#         self.clsbtn = QPushButton('Close', self)
#         self.foot.addWidget(self.clsbtn, 3)
#         self.clsbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
#         self.clsbtn.clicked.connect(self.close)

#         widget = QWidget()
#         widget.setLayout(self.layout)
#         self.setCentralWidget(widget)

#     @pyqtSlot()
#     def open_dialog(self, last_path) -> str:
#         """ open dialog browser and return file path """
#         dialog = QFileDialog(self)
#         dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
#         dialog.setNameFilter("ETABS Model Files(*.edb);;ETABS Model Files(*.EDB)")
#         dialog.setViewMode (QFileDialog.ViewMode.Detail)
#         dialog.setDirectory(last_path)
        
#         if dialog.exec():
#             filepathname= dialog.selectedFiles()
#             self.name=Path(filepathname[0])
            
#             if self.name == None:
#                 return False
#             else:
#                 print(f'in open dialog of view self.name is : {self.name}')
#                 return self.name
        
#         else: return False



class DriftWindow(QWidget):

    def __init__(self, etabs):
        super().__init__()
        # self.etabs = etabs
        self.drift_or_dis = ''
        
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Drift Window")
        
        #main layout
        main_vbox = QVBoxLayout()
        self.setLayout(main_vbox)
        
        #1st row
        hbox = QHBoxLayout()

        win_lable = QLabel('Drift Control Window')
        hbox.addWidget(win_lable)
        hbox.addSpacing(10)
        main_vbox.addLayout(hbox)

        #2nd row
        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        load_case_lbl = QLabel('Analysed Load Case:')
        hbox.addWidget(load_case_lbl)
        hbox.addStretch(1)
      
        self.drift_result_rbtn = QRadioButton('Drift')
        self.drift_result_rbtn.setChecked(True)
        self.drift_result_rbtn.toggled.connect(self.radio_button)
        hbox.addWidget(self.drift_result_rbtn)

        self.displacement_result_rbtn = QRadioButton('Displacement')
        self.displacement_result_rbtn.toggled.connect(self.radio_button)
        
        hbox.addWidget(self.displacement_result_rbtn)
        hbox.addSpacing(1)
        hbox.addStretch(1)

        self.load_label = QLabel('Load: Select Loade!')
        hbox.addWidget(self.load_label)
        main_vbox.addLayout(hbox)

        #3rd row
        hbox = QHBoxLayout()
        self.load_case_list = QListWidget()
        hbox.addWidget(self.load_case_list)

        #diaghram
        self.drift_plot= pg.plot()

        hbox.addWidget(self.drift_plot)

        #table
        self.result_table = QTableWidget()
        self.result_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) 
        self.result_table.setStyleSheet("font-size: 12px;"
                                               "font-weight: bold;")
        hbox.addWidget(self.result_table)
        main_vbox.addLayout(hbox)

        #4th row
        hbox = QHBoxLayout()
        self.select_load_btn = QPushButton('ُShow Results')
        hbox.addWidget(self.select_load_btn)
        hbox.addStretch(2)

        self.report_btn = QPushButton('Report')
        self.report_btn.setFixedSize(100, 40)
        hbox.addWidget(self.report_btn)
        
        hbox.addSpacing(1)
        cls_btn = QPushButton('Close')
        cls_btn.setFixedSize(70, 40)
        cls_btn.clicked.connect(self.close)
        hbox.addWidget(cls_btn)
        main_vbox.addLayout(hbox)
        self.radio_button()

    def radio_button(self):
        if self.drift_result_rbtn.isChecked():
            self.drift_or_dis = 'Story Drifts'
        if self.displacement_result_rbtn.isChecked():
            self.drift_or_dis = 'Story Max Over Avg Displacements' 

    def clicked(self):
        pass
    
    def graph(self, tb):
        data = tb.to_numpy()
        pg.plot(data, title="Simplest possible plotting example")
        print(f'data {data}')