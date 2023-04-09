from PyQt6.QtWidgets import QApplication, QMainWindow,  QTableWidgetItem
from PyQt6.QtCore import pyqtSlot
import sys
from pathlib import Path
import Home.Model as etabs
from Home.View import UI
from Drift.View import DriftWindow
import os
import numpy as np
import pandas as pd
import pyqtgraph as pg
import json
import Drift.Controller as drift_control
# from ..ETABS_Project import functions

# driftcntrl = Controller()
class ETABS(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = UI(self)
        self.window = DriftWindow(self)
        self.etabs = etabs.EtabsModel(self)
        self.drift_control = drift_control.ETABSDrift()
        self.folderpath = 'D:/'
        # self.connect_btn = self.view.connect_btn
        # self.statuslabel = self.view.statuslabel
        # self.prelabel = self.view.prelabel
        # self.driftbtn = self.view.driftbtn
        self.view.connect_btn.clicked.connect(self.open_etabs)
        self.name = self.etabs.connect_to_existing_file()
        print(f'connect shodam {self.name}')
        if self.name:
            print(f'self name is {self.name}')
            self.etabs.run_file
        
        self.etabs_load = list(self.etabs.get_load_cases())
        print(f' etabs load :  {self.etabs_load}')
        self.get_file_detaile()
        self.show_info()
        self.view.driftbtn.clicked.connect(self.toggle_window)
        self.view.driftbtn.clicked.connect(self.drift_check)
        # self.load_window()
        # self.window.select_load_btn.cl/icked.connect(self.drift_table)
        # self.window.select_load_btn.clicked.connect(self.graph)
            # self.window.select_load_btn.clicked.connect(self.graph)

    @pyqtSlot()
    def open_etabs(self) -> None:
        ame = self.view.open_dialog(self.folderpath)
        print(f'ame is {ame}')
        if ame is False:
            print('')
        else:
            self.name = ame
            self.show_info()
            self.get_file_detaile()
            self.etabs = etabs.EtabsModel(self.name)
            self.etabs.open_file()
            self.etabs.run_file
            # self.etabs.exit_file()

    def get_file_detaile(self) -> None:

        try:
            print('try detail')
            modelpath = str(Path(self.name))
            modelname = str(Path(os.path.basename(self.name)))
            etabspath = str(Path(etabs.EtabsModel(self.name).ProgramPath))
            self.folderpath = str(Path(os.path.dirname(self.name)))
            modelinfo = {
                "Model Name": modelname,
                "Model Path": modelpath,
                "ETABS Path": etabspath,
                "Folder Path": self.folderpath
            }
            with open("./Temp/model_info.json", "w+") as fp:
                json.dump(modelinfo, fp)
            self.view.statuslabel.setText(f'Connected to:  {modelname}')
        except TypeError:
            print('exept detail')
            pass

    def show_info(self) -> None:
        # try:
        print('show info is ')
        with open("./Temp/model_info.json", "r") as pdata:
            print(f'pdata is {pdata}')
            if pdata:
                data = json.load(pdata)
                datalist = []
                for i, j in data.items():
                    datalist.append(f'{i}:   {j}\n')

                self.view.prelabel.setText("".join(datalist))
                print("".join(datalist))
            else:
                print('nist')
        print(f'datalist is {datalist}')
        # except: print('nashod')

    def get_last_path(self) -> str:
        return str(self.name)

    def close_window(self):
        self.close()

    def toggle_window(self, checked):
        if self.window.isVisible():
            self.window.hide()

        else:
            self.window.show()

    def drift_check(self):
        print('drift checkkkkkkkkk')

        # fltrdload = functions.filtering(self.etabs_load, ("W", "EQ", "SPEC"))
        
        dataframe = self.etabs.get_data_table_outputs()
        print(f'data frame ine {dataframe} ')
        fltrdloads = list(filter(lambda x:  x.startswith(("W", "EQ", "SPEC")), self.etabs_load))
        self.drift_control.load_window(fltrdloads)
        self.etabs.select_load_cases(fltrdloads)
        print(f'load windo {fltrdloads}')
        
        
        # self.view.driftbtn.clicked.connect(self.toggle_window)
        self.window.select_load_btn.clicked.connect(lambda: self.drift_control.drift_table(self))
        # self.drift_control.error_on_drifttable()
        self.window.select_load_btn.clicked.connect(self.drift_control.graph)
        print('bade keshidane graph')



    # def filter_load(self, list, prefix: tuple) -> list:
    #     """
    #     give a list of strings and a tuple of prefix, filtered the list
    #     by items started with prefix
    #     """
    #     self.filtered_loads = filter(lambda x:  x.startswith(prefix), list)
    #     return self.filtered_loads


app = QApplication(sys.argv)
etabs1 = ETABS()
sys.exit(app.exec())
window = etabs1
window.show()
# app.exec()
