from pathlib import Path
import Home.Model as etabs
from Home.View import UI
import os
import json
import Drift.Controller as drift_control


class ETABS:

    def __init__(self):

        super().__init__()
        self.view = UI(self)
        self.etabs = etabs.EtabsModel(self)
        self.drift_control = drift_control.ETABSDrift()
        self.folderpath = 'D:/'

        self.view.connect_btn.clicked.connect(self.open_etabs)
        self.view.driftbtn.clicked.connect(self.toggle_window)
        self.drift_control = drift_control.ETABSDrift()
        self.drift_control.window.cls_btn.clicked.connect(self.max_drift_label)

        self.name = self.etabs.connect_to_existing_file()

        if self.name:
            self.etabs.run_file

        self.etabs_load = list(self.etabs.get_load_cases())
        self.get_file_detaile()
        self.show_info()

    # @pyqtSlot()
    def open_etabs(self) -> None:

        ame = self.view.open_dialog(self.folderpath)
        if ame is False:
            print('')
        else:
            self.name = ame
            self.show_info()
            self.get_file_detaile()
            self.etabs = etabs.EtabsModel(self.name)
            self.etabs.open_file()
            self.etabs.run_file()

    def get_file_detaile(self) -> None:

        try:
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
            pass

    def show_info(self) -> None:
        # try:

        with open("./Temp/model_info.json", "r") as pdata:

            if pdata:
                data = json.load(pdata)
                datalist = []
                for i, j in data.items():
                    datalist.append(f'{i}:   {j}\n')
                self.view.prelabel.setText("".join(datalist))
            else:
                print('nist')
        # except: print('nashod')

    def get_last_path(self) -> str:
        return str(self.name)

    def close_window(self):
        self.close()

    def toggle_window(self, checked):

        # self.drift_control = drift_control.ETABSDrift()
        if self.drift_control.window.isVisible():
            self.drift_control.window.hide()
        else:
            self.drift_control.window.show()
        self.drift_check()

    def drift_check(self):

        fltrdloads = list(filter(lambda x: x.startswith(("W", "EQ", "SPEC")), self.etabs_load))
        self.drift_control.load_window(fltrdloads)
        self.etabs.select_load_cases(fltrdloads)
        self.drift_control.window.export_btn.clicked.connect(lambda: self.drift_control.export_drift_xls())
        self.drift_control.window.load_case_list.itemClicked.connect(lambda: self.drift_control.drift_table(self.etabs))

        # msg = str(self.drift_control.max_drift_label_text())
        # print(type(msg), msg)
        # self.view.preres.setText(msg)

    def max_drift_label(self):

        self.drift_control.window.hide()
        self.view.preres.setText(self.drift_control.msg)
