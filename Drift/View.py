from PyQt6.QtWidgets import QWidget, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QTableWidget, QAbstractItemView
from PyQt6.QtCore import Qt, QItemSelectionModel
from PyQt6.QtGui import QCursor, QFont, QIcon, QStandardItemModel
import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtWidgets
# import pyqtgraph.exporters
# from PyQt6 import uic

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class DriftWindow(QWidget):

    def __init__(self, etabs):
        super().__init__()
        self.drift_or_dis = ''
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle("Drift Window")
        self.setWindowIcon(QIcon('ETABS_Project/utilities/ETABS1.png'))
        self.setStyleSheet("background-color : rgb(255,250,220);")

        # main layout
        main_vbox = QVBoxLayout()
        self.setLayout(main_vbox)

        # 1st row
        hbox = QHBoxLayout()
        win_lable = QLabel('Drift Control Window')
        hbox.addWidget(win_lable)
        hbox.addSpacing(10)
        main_vbox.addLayout(hbox)

        # 2nd row
        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        load_case_lbl = QLabel('Analysed Load Case:')
        hbox.addWidget(load_case_lbl)
        hbox.addStretch(1)

        self.drift_result_rbtn = QRadioButton('Drift')
        self.drift_result_rbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.drift_result_rbtn.setChecked(True)
        self.drift_result_rbtn.toggled.connect(self.radio_button)
        self.drift_result_rbtn.setEnabled(False)
        hbox.addWidget(self.drift_result_rbtn)

        self.displacement_result_rbtn = QRadioButton('Displacement')
        self.displacement_result_rbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.displacement_result_rbtn.toggled.connect(self.radio_button)
        self.displacement_result_rbtn.setEnabled(False)

        hbox.addWidget(self.displacement_result_rbtn)
        hbox.addSpacing(1)
        hbox.addStretch(1)

        self.load_label = QLabel('Load: Select Loade!')
        hbox.addWidget(self.load_label)
        main_vbox.addLayout(hbox)

        # 3rd row
        hbox = QHBoxLayout()
        self.load_case_list = QListWidget()
        self.load_case_list.setMaximumWidth(220)
        self.load_case_list.setMinimumWidth(180)
        self.load_case_list.setStyleSheet("background-color : white;")
        self.load_case_list.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        hbox.addWidget(self.load_case_list)

        # diaghram
        self.graphwin = pg.GraphicsLayoutWidget(show=True, title='Drift Control')
        self.graphwin.setMinimumWidth(400)
        hbox.addWidget(self.graphwin)

        # table
        self.result_table = QTableWidget()
        self.result_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.result_table.setMinimumWidth(350)
        self.result_table.setStyleSheet("font-size: 12px;""font-weight: bold;")
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setStyleSheet("background-color : white;")
        hbox.addWidget(self.result_table)
        main_vbox.addLayout(hbox)

        # 4th row
        hbox = QHBoxLayout()
        # self.export_btn = QPushButton('ُExcel Export')
        # self.export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # self.export_btn.hide()
        # hbox.addWidget(self.export_btn)
        hbox.addStretch(3)

        self.export_btn = QPushButton('Report')
        self.export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.export_btn.hide()
        self.export_btn.setFixedSize(100, 40)
        self.export_btn.setStyleSheet("border:1px solid rgb(170, 230, 190);")
        hbox.addWidget(self.export_btn)

        hbox.addSpacing(1)
        self.cls_btn = QPushButton('Close')
        self.cls_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cls_btn.setFixedSize(70, 40)
        self.cls_btn.setStyleSheet("border:1px solid rgb(170, 230, 190);")
        self.cls_btn.clicked.connect(self.close)

        hbox.addWidget(self.cls_btn)
        main_vbox.addLayout(hbox)

        # hbox = QHBoxLayout()
        # self.prelbl = QLabel('pre drift info')
        # self.prelbl.setFont(QFont('Arial', 2))
        # self.prelbl.setAlignment(Qt.AlignmentFlag.AlignBottom)
        # hbox.addWidget(self.prelbl)
        # hbox.addStretch(5)
        # main_vbox.addLayout(hbox)

        # footer
        hbox = QHBoxLayout()
        self.maxdrift_lbl = QLabel('max drift info')
        self.maxdrift_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.maxdrift_lbl.setFont(QFont('Arial', 8))
        self.maxdrift_lbl.setMaximumHeight(20)
        self.maxdrift_lbl.setStyleSheet(u"background: lightblue")
        hbox.addWidget(self.maxdrift_lbl)
        main_vbox.addLayout(hbox)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        self.radio_button()

    def radio_button(self):

        if self.drift_result_rbtn.isChecked():
            self.drift_or_dis = 'Story Drifts'
        if self.displacement_result_rbtn.isChecked():
            self.drift_or_dis = 'Story Max Over Avg Displacements'

    def graph(self, tb):

        data = tb.to_numpy()
        pg.plot(data, title="Simplest possible plotting example")
        print(f'data {data}')
