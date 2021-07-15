import os
import time
from pdftoxmlGUI import extract_files
import pandas as pd

def get_last_or_second_last_modify_file(all_path_to_analyse):
    array_path = []
    for path in all_path_to_analyse:
        fileStatsObj = os.stat(path)
        modificationTime = time.ctime(fileStatsObj.st_mtime)
        #modificationTime = fileStatsObj.st_mtime
        # print(modificationTime)
        array_path.append([os.path.dirname(path),path,modificationTime])
    data_to_filter = pd.DataFrame(array_path,columns=['directory','path','time_modify'])
    data_to_filter['time_modify'] = pd.to_datetime(data_to_filter['time_modify'])
    data_to_filter.sort_values(by=['directory','time_modify'], inplace=True, ascending=[True, False])

    #pd.set_option('display.max_colwidth', -1)
    #pd.set_option('display.max_columns', None)
    #print(data_to_filter)
    data_to_filter = data_to_filter.groupby(by='directory').head(2)
    data_to_filter = data_to_filter[data_to_filter['path'].str.contains('invoice') == False]


    return data_to_filter['path'].tolist()


path = "C:\\Users\\Asus\\Desktop\\CaPIimmobilier\\CaPIimmobilier\\données\\01-03-2021\\Complet avec revenu"
files_to_analyze = extract_files(path,".pdf")
data = get_last_or_second_last_modify_file(files_to_analyze)

