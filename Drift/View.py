from PyQt6.QtWidgets import QWidget, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QTableWidget, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
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
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Drift Window")

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
        hbox.addWidget(self.drift_result_rbtn)

        self.displacement_result_rbtn = QRadioButton('Displacement')
        self.displacement_result_rbtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.displacement_result_rbtn.toggled.connect(self.radio_button)

        hbox.addWidget(self.displacement_result_rbtn)
        hbox.addSpacing(1)
        hbox.addStretch(1)

        self.load_label = QLabel('Load: Select Loade!')
        hbox.addWidget(self.load_label)
        main_vbox.addLayout(hbox)

        # 3rd row
        hbox = QHBoxLayout()
        self.load_case_list = QListWidget()
        self.load_case_list.setMaximumWidth(180)
        self.load_case_list.setMinimumWidth(120)
        hbox.addWidget(self.load_case_list)

        # diaghram
        self.graphwin = pg.GraphicsLayoutWidget(show=True, title='Drift Control')
        self.graphwin.setMinimumWidth(400)
        hbox.addWidget(self.graphwin)

        # table
        self.result_table = QTableWidget()
        self.result_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.result_table.setMinimumWidth(300)
        self.result_table.setStyleSheet("font-size: 12px;""font-weight: bold;")
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
        self.export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        hbox.addWidget(self.export_btn)

        hbox.addSpacing(1)
        self.cls_btn = QPushButton('Close')
        self.cls_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cls_btn.setFixedSize(70, 40)

        hbox.addWidget(self.cls_btn)
        main_vbox.addLayout(hbox)
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
