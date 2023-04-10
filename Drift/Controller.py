from PyQt6.QtWidgets import QTableWidgetItem, QListWidgetItem
from PyQt6.QtCore import pyqtSlot
from Drift.View import DriftWindow
import numpy as np
import pandas as pd
import pyqtgraph as pg
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import  ColorScaleRule
import ETABS_Project.functions as func
# from Home.Controller import ETABS


class ETABSDrift:
    def __init__(self):
        # super().__init__()
        self.window = DriftWindow(self)
        self.load_table_xy = pd.DataFrame()

    # use loads and fill the load list
    def load_window(self, drift_data: list):

        for index, value in enumerate(drift_data):
            self.window.load_case_list.insertItem(index, value)
            item = QListWidgetItem(value)
            self.window.load_case_list.addItem(item)
            print(value)

    def drift_table(self, etabsobj):

        self.driftload = self.window.load_case_list.currentItem()
        selected_load = self.driftload.text()
        selected_table = self.window.drift_or_dis
        story_drifts_table = etabsobj.etabs.get_data_table_outputs(table_key=selected_table)
        self.window.load_label.setText(f'Load: {selected_load}')
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
                load_table=None

        # reset index change previous index to 0-1-2-3-.... and use previouse index as a column
        self.load_table_xy.reset_index(inplace=True)

        # replace Nan values with zero
        self.load_table_xy.fillna(0, inplace=True)
        self.temp = self.load_table_xy
        self.row_no = self.load_table_xy['X'].size


        if load_table is None:
            self.error_on_drifttable()
            
        else:
            self.window.result_table.setColumnCount(3)
            self.window.result_table.setRowCount(self.row_no)
            

            for row in range(self.row_no):
                for col in range(3):
                    litem = (self.load_table_xy.iloc[row][col])

                    self.window.result_table.setItem(row, col, QTableWidgetItem(litem))
            self.graph()
            
        self.window.result_table.setHorizontalHeaderLabels(['Story', self.tableitem + "\nX", self.tableitem  + "\nY"])

    def error_on_drifttable(self):
        self.window.result_table.clear()
        self.window.graphwin.clear()

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

        penx = pg.mkPen({'color': "g", 'width': 3})
        peny = pg.mkPen({'color': "b", 'width': 3})
        penlimit = pg.mkPen({'color': "r", 'width': 3})
        stringaxis = pg.AxisItem(orientation='left')
        stringaxis.setTicks([list(dict(enumerate(lstring)).items())])

        self.window.graphwin.clear()
        drift_graph = self.window.graphwin.addPlot(title = 'Drift Control')
        drift_graph.addLegend()
        drift_graph.showGrid(x=True, y=True)
        drift_graph.setLabel('left', 'Story', units=None)
        drift_graph.setLabel('bottom', self.tableitem)
        drift_graph.setXRange(0, 0.003)
        drift_graph.setYRange(0, 7)
        drift_graph.setAxisItems(axisItems={'left': stringaxis})
        drift_graph.plot(datax, title=self.tableitem + ' X', symbol='o', symbolPen='g', pen=penx, name='Drift X' )
        drift_graph.plot(datay, title=self.tableitem + ' Y', symbol='o', symbolPen='b', pen=peny, name='Drift Y')
        drift_graph.plot(datalimit, title=self.tableitem + ' Limit', pen=penlimit, name='Limit')
       
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
        