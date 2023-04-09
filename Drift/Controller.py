from PyQt6.QtWidgets import QApplication, QMainWindow,  QTableWidgetItem
from PyQt6.QtCore import pyqtSlot
import sys
from pathlib import Path
import Drift.Model as etabs
# import Drift.View
from Drift.View import DriftWindow
import os
import numpy as np
import pandas as pd
import pyqtgraph as pg
import json
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScale, FormatObject, ColorScaleRule
from openpyxl.styles import Color
import ETABS_Project.functions as func
# from Home.Controller import ETABS


class ETABSDrift:
    def __init__(self):
        # super().__init__()
        # self.view = UI(self)
        # self.folderpath = 'D:/'
        # self.connect_btn = self.view.connect_btn
        # self.statuslabel = self.view.statuslabel
        # self.prelabel = self.view.prelabel
        # self.driftbtn = self.view.driftbtn
        # self.connect_btn.clicked.connect(self.open_etabs)
        # self.etabs = etabs.DriftModel(self)
        # self.etabs = etabs.DriftModel()
        # self.show_info()
        # self.name = self.etabs.connect_to_existing_file()
        # if self.name:
        #     self.etabs.run_file()
        # self.etabs_load = list(self.etabs.get_load_cases())
        # self.get_file_detaile()
        self.window = DriftWindow(self)
        self.load_table_xy = pd.DataFrame()

        # self.view.driftbtn.clicked.connect(self.toggle_window)
        # self.load_window()
        # self.window.select_load_btn.clicked.connect(self.drift_table)
        # self.window.select_load_btn.clicked.connect(self.graph)
        # self.window.select_load_btn.clicked.connect(self.graph)

    

    # use loads and fill the load list
    def load_window(self, drift_data: list):

        # for index, value in enumerate(drift_data):
            # self.window.load_case_list.insertItem(index, value)
            # item = QListWidgetItem(value)
            # self.window.load_case_list.addItem(item)
            # print(value)

        self.window.load_case_table.setColumnCount(1)
        self.window.load_case_table.setRowCount(len(drift_data))

        for n in range(len(drift_data)):
            
            lqitem = drift_data[n]
            self.window.load_case_table.setItem(n ,0 ,QTableWidgetItem(lqitem))
            print(lqitem)
        
        # self.etabs.select_load_cases(fltdrfload)

    def drift_table(self, etabsobj):

        # self.driftload = self.window.load_case_list.currentItem()
        self.driftload = "SPECXY_ND"
        # selected_load = self.driftload.text()
        selected_load = self.driftload
        selected_table = self.window.drift_or_dis
        story_drifts_table = etabsobj.etabs.get_data_table_outputs(table_key=selected_table)
        # query desiered columns
        load_drift = story_drifts_table[story_drifts_table.OutputCase == selected_load]

        if selected_table == 'Story Drifts':
            load_table = load_drift[['Story', 'Direction', 'Drift']]
            kvalue = "Drift"
            self.tableitem = 'Drift'
        elif selected_table == 'Story Max Over Avg Displacements':
            load_table = load_drift[['Story', 'Direction', 'Maximum']]
            kvalue = "Maximum"
            self.tableitem = 'Displacement'

        # pivot load table to transfer Direction column to X and Y column
        self.load_table_xy = load_table.pivot(columns="Direction", values=kvalue, index='Story')
        
        # check if there is not any Y load make a new column calls Y with 0 values
        if "Y" not in self. load_table_xy.columns:
            self.load_table_xy['Y'] = 0

        if "X" not in self.load_table_xy.columns:
            self.load_table_xy['X']=0

            # arrange column
            if "Story" in self.load_table_xy.columns:
                self.load_table_xy = self.load_table_xy[['Story', 'X', 'Y']]
            else:
                self.load_table_xy = pd.DataFrame(np.zeros([8, 3]), columns=('Story', 'X', 'Y'))

        # reset index change previous index to 0-1-2-3-.... and use previouse index as a column
        self.load_table_xy.reset_index(inplace=True)

        # replace Nan values with zero
        self.load_table_xy.fillna(0, inplace=True)
        self.temp = self.load_table_xy
        self.row_no = self.load_table_xy['X'].size

        if self.row_no == 0:
            self.error_on_drifttable()
        else:
            self.window.result_table.setColumnCount(3)
            self.window.result_table.setRowCount(self.row_no)

            for row in range(self.row_no):
                for col in range(3):
                    litem = self.load_table_xy.iloc[row][col]
                    self.window.result_table.setItem(row, col, QTableWidgetItem(litem))
            self.window.load_label.setText(f'Load: {selected_load}')
        self.window.result_table.setHorizontalHeaderLabels(['Story', self.tableitem + "\nX", self.tableitem +"\nY"])

    def error_on_drifttable(self):
        self.window.result_table.setColumnCount(3)
        self.window.result_table.setRowCount(8)

    def graph(self):

        # get int from str column
        lstring = self.load_table_xy['Story'].tolist()
        dict_lstring = list(dict(enumerate(lstring)).keys())
        valuelistx = self.load_table_xy['X'].tolist()
        valuelisty = self.load_table_xy['Y'].tolist()
        # transpose table
        datax = pd.DataFrame(np.array([valuelistx, dict_lstring], dtype=float)).T.to_numpy()
        datay = pd.DataFrame(np.array([valuelisty, dict_lstring], dtype=float)).T.to_numpy()
        datalimit = np.array([[0.002, 0], [0.002, 1], [0.002, 2], [0.002, 3], [0.002, 4], [0.002, 5], [0.002, 6]])
        print(f'data is \n {datax}')
        print(datax.shape)

        penx = pg.mkPen({'color': "g", 'width': 3})
        peny = pg.mkPen({'color': "b", 'width': 3})
        penlimit = pg.mkPen({'color': "r", 'width': 3})
        stringaxis = pg.AxisItem(orientation='left')
        stringaxis.setTicks([list(dict(enumerate(lstring)).items())])

        self.window.drift_plot.clear()
        self.window.drift_plot.addLegend()
        self.window.drift_plot.showGrid(x=True, y=True)
        self.window.drift_plot.setLabel('left', 'Story', units=None)
        self.window.drift_plot.setLabel('bottom', self.tableitem)
        self.window.drift_plot.setXRange(0, 0.003)
        self.window.drift_plot.setYRange(0, 7)
        self.window.drift_plot.setAxisItems(axisItems={'left': stringaxis})
        self.window.drift_plot.plot(datax, title=self.tableitem + ' X', symbol='o', symbolPen='g', pen=penx, name='Drift X' )
        self.window.drift_plot.plot(datay, title=self.tableitem + ' Y', symbol='o', symbolPen='b', pen=peny, name='Drift Y')
        self.window.drift_plot.plot(datalimit, title=self.tableitem + ' Limit', pen=penlimit, name='Limit')
        self.export_drift_xls()

    def export_drift_xls(self):

        wb = Workbook()
        ws = wb.active
        ws.append(['Story', 'X', 'Y'])

        # fill data of dirfts to excel table by making list
        for rowindex in range(self.row_no):
            row = func.strlist_to_floatlist(list(self.load_table_xy.iloc[rowindex]))
            ws.append(row)

        # use local module to named excell cells with rows and cols number
        ref = func.rowcol_to_xlsxcell(1 ,1 ,3 ,self.row_no+1)
        tab = Table(displayName="Table1", ref=ref)

        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                            showLastColumn=False, showRowStripes=True, showColumnStripes=True)

        tab.tableStyleInfo = style
        ws.add_table(tab)

        rule = ColorScaleRule(start_type='num', start_value=0.002, start_color='FF00AA00',
                              mid_type='num', mid_value=0.001, mid_color='9d52ff',
                              end_type='num', end_value=0.002, end_color='FFAA0000')
        ws.conditional_formatting.add(ref, rule)

        wb.save("Drift_Check.xlsx")