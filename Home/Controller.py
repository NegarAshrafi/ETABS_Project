import os
import json
from pathlib import Path
import Home.Model as etabs
from ETABS_Project.Home.Wellcome_View import WellcomeWindow
import Drift.Controller as drift_control


class ETABS:

    def __init__(self):

        super().__init__()
        self.wellcome = WellcomeWindow(self)
        self.wellcome.show()
        self.etabs = etabs.EtabsModel(self)
        self.drift_control = drift_control.ETABSDrift()
        self.folderpath = 'D:/'

        self.wellcome.new_file_btn.clicked.connect(self.open_etabs)
        self.wellcome.connect_btn.clicked.connect(self.connect_etabs)

        self.wellcome.run_drift_btn.clicked.connect(self.toggle_window)
        self.etabs_load = list(self.etabs.get_load_cases())

    def open_etabs(self) -> None:

        name = self.wellcome.open_dialog(self.folderpath)
        if name is False:
            print('')
        else:
            self.name = name
            self.etabs = etabs.EtabsModel(self.name)
            self.etabs.open_file()
        # self.wellcome.run_btn.setEnabled(True)
        self.wellcome.setWindowTitle(f"ETABS API-{self.name}")
        self.connect_etabs()

    def connect_etabs(self):

        try:
            self.name = self.etabs.connect_to_existing_file()
            print('try')
            # self.wellcome.run_btn.setEnabled(True)
            self.wellcome.setWindowTitle(f"ETABS API-  {str(Path(os.path.basename(self.name)))}")
            self.drift_control = drift_control.ETABSDrift()
            # self.drift_control.window.cls_btn.clicked.connect(self.max_drift_label)
            self.etabs_load = list(self.etabs.get_load_cases())
            self.get_file_detaile()
            self.show_info()
            self.check_run()
            # self.view.clsbtn.clicked.connect(lambda: self.wellcome.show())

        except AttributeError:
            print('wrror')
            self.wellcome.active_file()

    def check_run(self):
        msg = str(self.etabs.check_run())
        self.check_msg = 'drift check'
        if msg == "run_needed":
            self.check_msg = 'run'
            self.wellcome.run_drift_btn.setText('Run')
            
        self.wellcome.run_drift_btn.setEnabled(True)

    def run_etabs(self):

        self.check_msg = self.etabs.run_file()
        self.wellcome.run_drift_btn.setText('Check Drift')
        self.wellcome.run_drift_btn.setEnabled(True)

    def get_file_detaile(self) -> None:

        try:
            modelpath = str(Path(self.name))
            self.modelname = str(Path(os.path.basename(self.name)))
            self.etabspath = str(Path(etabs.EtabsModel(self.name).ProgramPath))
            self.folderpath = str(Path(os.path.dirname(self.name)))
            modelinfo = {
                "Model Name": self.modelname,
                "Model Path": modelpath,
                "ETABS Path": self.etabspath,
                "Folder Path": self.folderpath
            }
            with open("./Temp/model_info.json", "w+") as fp:
                json.dump(modelinfo, fp)
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
                # self.wellcome.preetabs.setText("".join(datalist))
                self.wellcome.preetabs.setText(data["Model Path"])
                self.wellcome.etabs_path.setText(data["ETABS Path"])
            else:
                print('nist')
        # except: print('nashod')

    def get_last_path(self) -> str:
        return str(self.name)

    def close_window(self):
        self.close()

    def toggle_window(self, checked):

        if self.check_msg == 'run':
            self.run_etabs()
        else:
            self.drift_control = drift_control.ETABSDrift()
            if self.drift_control.window.isVisible():
                self.drift_control.window.hide()
            else:
                self.drift_control.window.show()
            self.drift_control.get_drift_table(self.etabs)
            self.drift_check()

    def drift_check(self):

        fltrdloads = list(filter(lambda x: x.startswith(("W", "EQ", "SPEC")), self.etabs_load))
        self.etabs.select_load_cases(fltrdloads)
        self.drift_control.window.export_btn.clicked.connect(lambda: self.drift_control.export_drift_xls())
        self.drift_control.window.load_case_list.itemClicked.connect(lambda: self.drift_control.drift_table())
        self.drift_control.window.drift_result_rbtn.toggled.connect(lambda: self.drift_control.drift_table())
        # self.drift_control.window.maxdrift_lbl.setText(self.drift_control.msg)
        # msg = str(self.drift_control.max_drift_label_text())
        # print(type(msg), msg)
        # self.view.preres.setText(msg)

    # def max_drift_label(self):

    #     self.drift_control.window.hide()
    #     self.drift_control.window.prelbl.setText(self.drift_control.msg)
