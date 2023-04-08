import sys
import comtypes.client
from pathlib import Path
import pandas as pd
from Home import Model as mainmodel


class DriftModel:
    def __init__(self, filepath=None) -> None:
        self.derif_data = "Story Drift"
        # super.__init__()
        # self.ModelPath = filepath
        # self.ProgramPath = "C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"
        # self.helper = None
        # self.myETABSObject = None
        # self.software_exe_path = ''
        # self.SapModel = None

    # def get_data_table_outputs(self, table_key = "Story Drifts"):
    #     """
    #     output is pandas DataFrame type. a data table just like Show Tables at Etabs
    #     """
    #     all_table = self.SapModel.DatabaseTables.GetAvailableTables()[1]

    #     if table_key in all_table:
    #         print(f'there is table key ')
    #     else:
    #         print('there is not table key')

    #     GroupName = table_key
    #     FieldKeyList = []
    #     TableVersion = 0
    #     FieldsKeysIncluded = []
    #     NumberRecords = 0
    #     TableData = []
    #     ret = self.SapModel.DatabaseTables.GetTableForDisplayArray(table_key, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
    #     _, _, FieldsKeysIncluded, _, TableData, _ = ret
    #     n = len(FieldsKeysIncluded)
    #     tabledata_no = len(TableData)
    #     self.column_no = len(FieldsKeysIncluded)
    #     self.row_no = int(tabledata_no / self.column_no)

    #     # print(TableData)
    #     i = 0
    #     mydict = {}
    #     for item in iter(FieldsKeysIncluded):
    #         listhelp = []
    #         for n in range(i, tabledata_no, self.column_no):
    #             listhelp.append(TableData[n])
    #         mydict[item] = listhelp
    #         i += 1

    #     data_frame = pd.DataFrame(mydict, columns=FieldsKeysIncluded)
    #     return data_frame
    
