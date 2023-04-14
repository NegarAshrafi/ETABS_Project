from PyQt6.QtWidgets import QTableWidgetItem, QListWidgetItem
from Drift.View import DriftWindow
import numpy as np
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.exporters
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.drawing.image import Image
import functions as func


class ETABSDrift:

    def __init__(self):
        self.window = DriftWindow(self)
        self.load_table_xy = pd.DataFrame()
        self.msg = ""

    # use loads and fill the load list
    def load_window(self, drift_data: list):

        for index, value in enumerate(drift_data):
            self.window.load_case_list.insertItem(index, value)
            item = QListWidgetItem(value)
            self.window.load_case_list.addItem(item)

    def drift_table(self, etabsobj):

        self.driftload = self.window.load_case_list.currentItem()
        self.selected_load = self.driftload.text()
        self.window.drift_result_rbtn.setEnabled(True)
        self.window.displacement_result_rbtn.setEnabled(True)
        self.window.drift_result_rbtn.toggled.connect(self.window.radio_button)
        selected_table = self.window.drift_or_dis
        story_drifts_table = etabsobj.get_data_table_outputs(table_key=selected_table)
        self.window.load_label.setText(f'Load: {self.selected_load}')
        # query desiered columns
        load_drift = story_drifts_table[story_drifts_table.OutputCase == self.selected_load]

        story_definitions_table = etabsobj.get_data_table_outputs(table_key="Story Definitions")
        
        # project total height
        self.height = story_definitions_table['Height'].astype(float).sum()

        if selected_table == 'Story Drifts':
            load_table = load_drift[['Story', 'Direction', 'Drift']]
            kvalue = "Drift"
            self.tableitem = 'Drift'
        elif selected_table == 'Story Max Over Avg Displacements':
            load_table = load_drift[['Story', 'Direction', 'Maximum']]
            kvalue = "Maximum"
            self.tableitem = 'Displacement'

        # pivot load table to transfer Direction column to X and Y column
        self.load_table_xy = load_table.pivot_table(columns="Direction", values=kvalue, index='Story', sort=False)

        # check if there is not any Y load make a new column calls Y with 0 values
        if "Y" not in self. load_table_xy.columns:
            self.load_table_xy['Y'] = 0

        if "X" not in self.load_table_xy.columns:
            self.load_table_xy['X'] = 0

            # arrange column
            if "Story" in self.load_table_xy.columns:
                self.load_table_xy = self.load_table_xy[['Story', 'X', 'Y']]

            else:
                self.load_table_xy = pd.DataFrame(np.zeros([8, 3]), columns=('Story', 'X', 'Y'))
                load_table = None

        # reset index change previous index to 0-1-2-3-.... and use previouse index as a column
        self.load_table_xy.reset_index(inplace=True)

        # replace Nan values with zero
        self.load_table_xy.fillna(0, inplace=True)

        # add basement floor to list
        self.load_table_xy.loc[len(self.load_table_xy.index)] = ["Bs", 0, 0]
        self.row_no = self.load_table_xy['X'].size
        self.load_table_xy = self.load_table_xy.iloc[::-1]
        self.temp = self.load_table_xy
        # self.row_no = self.load_table_xy['X'].size

        if load_table is None:
            self.error_on_drifttable()

        else:
            self.window.result_table.setColumnCount(3)
            self.window.result_table.setRowCount(self.row_no)

            for row in range(self.row_no):
                for col in range(3):
                    litem = str(self.load_table_xy.iloc[row][col])

                    self.window.result_table.setItem(row, col, QTableWidgetItem(litem))
            self.graph()

        self.window.result_table.setHorizontalHeaderLabels(['Story', self.tableitem + "\nX", self.tableitem + "\nY"])
        self.window.maxdrift_lbl.setText(self.msg)

    def error_on_drifttable(self):

        self.window.result_table.clear()
        self.window.graphwin.clear()

    def graph(self):

        # get int from str column
        # self.load_table_xy = self.load_table_xy.iloc[::-1]
        lstring = self.load_table_xy['Story'].tolist()
        dict_lstring = list(dict(enumerate(lstring)).keys())
        valuelistx = self.load_table_xy['X'].tolist()
        valuelisty = self.load_table_xy['Y'].tolist()

        self.maxdriftx = str(max(func.strlist_to_floatlist(valuelistx)))
        self.maxdrifty = str(max(func.strlist_to_floatlist(valuelisty)))

        # transpose table
        datax = pd.DataFrame(np.array([valuelistx, dict_lstring], dtype=float)).T.to_numpy()
        datay = pd.DataFrame(np.array([valuelisty, dict_lstring], dtype=float)).T.to_numpy()
        datalimit = np.array([[0.002, x] for x in range(self.row_no-1)]) if self.tableitem == "Drift" else np.array([[0, 0], [self.height * 0.002, self.row_no-1]])

        penx = pg.mkPen({'color': "g", 'width': 3})
        peny = pg.mkPen({'color': "b", 'width': 3})
        penlimit = pg.mkPen({'color': "r", 'width': 3})
        stringaxis = pg.AxisItem(orientation='left')
        stringaxis.setTicks([list(dict(enumerate(lstring)).items())])

        self.window.graphwin.clear()
        self.drift_graph = self.window.graphwin.addPlot()
        self.drift_graph.addLegend()
        self.drift_graph.addItem
        self.drift_graph.showGrid(x=True, y=True, alpha=0.5)
        self.drift_graph.setLabel('left', 'Story', units=None)
        self.drift_graph.setLabel('bottom', self.tableitem)
        self.drift_graph.setAxisItems(axisItems={'left': stringaxis})
        self.drift_graph.plot(datax, title=self.tableitem + ' X', symbol='o', symbolPen='g', pen=penx, name='Drift X')
        self.drift_graph.plot(datay, title=self.tableitem + ' Y', symbol='o', symbolPen='b', pen=peny, name='Drift Y')
        self.drift_graph.plot(datalimit, title=self.tableitem + ' Limit', pen=penlimit, name='Limit')
        self.window.export_btn.show()
        self.window.export_btn.setEnabled(True)
        self.window.export_btn.setText('Report')

        self.msg = f' LC: {self.selected_load}: ->  Max {self.tableitem} X = {self.maxdriftx},  Max {self.tableitem} Y = {self.maxdrifty}'

    def export_drift_xls(self):

        # export graph as png image
        g_exporter = pg.exporters.ImageExporter(self.drift_graph)
        g_exporter.export('ETABS_Project/Temp/plot.png')

        wb = Workbook()
        ws = wb.active
        ws.append(['Story', 'X', 'Y'])

        # fill data of dirfts to excel table by making list
        for rowindex in range(self.row_no):
            row = func.strlist_to_floatlist(list(self.load_table_xy.iloc[rowindex]))
            ws.append(row)

        # use local module to named excell cells with rows and cols number
        ref = func.rowcol_to_xlsxcell(1, 1, 3, self.row_no + 1)
        tab = Table(displayName="Table1", ref=ref)

        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=True)

        tab.tableStyleInfo = style
        ws.add_table(tab)

        rule = ColorScaleRule(start_type='num', start_value=0.002, start_color='FF00AA00',
                              mid_type='num', mid_value=0.001, mid_color='9d52ff',
                              end_type='num', end_value=0.002, end_color='FFAA0000')
        ws.conditional_formatting.add(ref, rule)

        # add graph image to excel 
        graph_img = Image('ETABS_Project/Temp/plot.png')
        ws.add_image(graph_img, 'E1')

        wb.save("ETABS_Project/Reports/Drift_Check.xlsx")
        self.window.export_btn.setText('Reported Successfully!')
        self.window.export_btn.setFixedSize(150, 40)
        self.window.export_btn.setDisabled(True)
