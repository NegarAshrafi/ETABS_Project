import sys
import time
import comtypes.client
from pathlib import Path
import pandas as pd
# from Drift.Model import DriftModel


class EtabsModel:

    def __init__(self, filepath=None) -> None:
        self.ModelPath = filepath
        self.ProgramPath = "C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"
        self.helper = None
        self.myETABSObject = None
        self.software_exe_path = ''
        self.SapModel = None

    def connect_to_existing_file(self) -> str:

        """ If an Etabs file is in the process this method will connect the app to that and return the path of its file"""
        try:
            self.myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
            self.SapModel = self.myETABSObject.SapModel

        except (OSError, comtypes.COMError):
            self.success = False
            # sys.exit(-1)
            if self.myETABSObject is None:
                helper = comtypes.client.CreateObject('ETABSv1.Helper')
                helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

            if hasattr(helper, 'GetObjectProcess'):
                try:
                    import psutil
                except ImportError:
                    import subprocess
                    package = 'psutil'
                    subprocess.check_call(["pip", "install", package])
                    import psutil
                pid = None

                for proc in psutil.process_iter():

                    if "ETABS" in proc.name().lower():
                        pid = proc.pid
                        break

                if pid:
                    self.myETABSObject = helper.GetObjectProcess("CSI.ETABS.API.ETABSObject", pid)
                    self.success = True
        self.SapModel = self.myETABSObject.SapModel
        self.name = Path(self.SapModel.GetModelFilename())
        return self.name

    def open_file(self):
        # create API helper object
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

        try:
            # create an instance of the ETABS object from the latest installed ETABS
            self.myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program.")
            sys.exit(-1)

            # start ETABS application
        self.myETABSObject.ApplicationStart()

        # create SapModel object
        self.SapModel = self.myETABSObject.SapModel

        # initialize model
        self.SapModel.InitializeNewModel()
        # create new blank model
        self.SapModel.File.OpenFile(str(self.ModelPath))

    def check_run(self) -> str:
        """
        check if all load cases are analyzed or not and return 'run_needed' string if it needs run"""
        case_status = self.get_case_status()
        templist = [a for a in case_status if a == 4]
        if len(case_status) > len(templist):
            return "run_needed"

    def run_file(self) -> bool:
        """
        check if all loads analyze are complete returns finished, else starts analyze and when complete returns finished"""

        # run model (this will create the analysis model)
        ret = self.SapModel.Analyze.RunAnalysis()
        check_msg = 'analysis is completed'
        return check_msg

    def get_case_status(self) -> tuple:
        """ meaning of numbers at self. case_status:
            status = {1: "Not run",
                    2: "Could not start",
                    3: "Not finished",
                    4: "Finished"} 
                    """
        self.case_status = self.SapModel.Analyze.GetCaseStatus()[2]
        return self.case_status

    def get_file_path(self):

        self.path = Path(self.SapModel.GetModelFilename()).parent
        return self.path

    def exit_file(self):

        try:
            self.SapModel.ApplicationExit(False)
        except AttributeError:
            pass

        self.SapModel = None
        self.myETABSObject = None

    def get_load_cases(self) -> list:

        try:
            lcnames = self.SapModel.LoadCases.GetNameList(0, [])[1]
            return lcnames
        except (AttributeError, TypeError):
            return []

    def select_load_cases(self, names):

        self.SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay('')
        self.SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(names)

    def get_data_table_outputs(self, table_key="Story Drifts") -> pd.DataFrame:
        """
        output is pandas DataFrame type. a data table just like Show Tables at Etabs
        """

        GroupName = table_key
        FieldKeyList = []
        TableVersion = 0
        FieldsKeysIncluded = []
        NumberRecords = 0
        TableData = []
        ret = self.SapModel.DatabaseTables.GetTableForDisplayArray(table_key, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        _, _, FieldsKeysIncluded, _, TableData, _ = ret
        n = len(FieldsKeysIncluded)
        tabledata_no = len(TableData)
        self.column_no = len(FieldsKeysIncluded)
        self.row_no = int(tabledata_no / self.column_no)

        i = 0
        mydict = {}
        for item in iter(FieldsKeysIncluded):
            listhelp = []
            for n in range(i, tabledata_no, self.column_no):
                listhelp.append(TableData[n])
            mydict[item] = listhelp
            i += 1

        data_frame = pd.DataFrame(mydict, columns=FieldsKeysIncluded)
        return data_frame
