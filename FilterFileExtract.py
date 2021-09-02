import os
import time
import re
from pdftoxmlGUI import extract_files
import pandas as pd


def get_last_or_second_last_modify_file(all_path_to_analyse, reason_form):
    array_path = []
    for path in all_path_to_analyse:
        fileStatsObj = os.stat(path)
        modificationTime = time.ctime(fileStatsObj.st_mtime)
        # modificationTime = fileStatsObj.st_mtime
        # print(modificationTime)
        array_path.append([os.path.dirname(path), path, modificationTime])
    data_to_filter = pd.DataFrame(array_path, columns=['directory', 'path', 'time_modify'])
    data_to_filter['time_modify'] = pd.to_datetime(data_to_filter['time_modify'])
    data_to_filter.sort_values(by=['directory', 'time_modify'], inplace=True, ascending=[True, False])

    # pd.set_option('display.max_colwidth', -1)
    # pd.set_option('display.max_columns', None)
    # print(data_to_filter)
    data_to_filter = data_to_filter.groupby(by='directory').head(2)
    remove_string_in_path =['invoice','honos', 'demande originale', 'scan','facture', 'Demandes annulées', 'permis']
    # data_to_filter = data_to_filter[data_to_filter['path'].str.contains('invoice', flags=re.IGNORECASE, regex=True) == False]
    # #data_to_filter = data_to_filter[data_to_filter['path'].str.contains('Invoice') == False]
    # data_to_filter = data_to_filter[data_to_filter['path'].str.contains('honos', flags=re.IGNORECASE, regex=True) == False]
    # data_to_filter = data_to_filter[data_to_filter['path'].str.contains('demande originale', flags=re.IGNORECASE, regex=True) == False]
    # data_to_filter = data_to_filter[
    #     data_to_filter['path'].str.contains('scan', flags=re.IGNORECASE, regex=True) == False]
    # data_to_filter = data_to_filter[
    #     data_to_filter['path'].str.contains('facture', flags=re.IGNORECASE, regex=True) == False]
    # data_to_filter = data_to_filter[
    #     data_to_filter['path'].str.contains('Demandes annulées', flags=re.IGNORECASE, regex=True) == False]
    # data_to_filter = data_to_filter[
    #     data_to_filter['path'].str.contains('permis', flags=re.IGNORECASE, regex=True) == False]

    for string in remove_string_in_path:
        add_reason_to_delete_path(string, data_to_filter, reason_form)
        data_to_filter = data_to_filter[
            data_to_filter['path'].str.contains(string, flags=re.IGNORECASE, regex=True) == False]

    return data_to_filter['path'].tolist()


# path = "C:\\Users\\Asus\\Desktop\\CaPIimmobilier\\CaPIimmobilier\\données\\01-03-2021\\Complet avec revenu"
# files_to_analyze = extract_files(path,".pdf")
# data = get_last_or_second_last_modify_file(files_to_analyze)

def extract_number_sublevel(pdfFiles, path, number_level):
    number_default = path.count("\\")
    count_to_verify = number_level + number_default
    path_to_verify = []
    for pdfFile in pdfFiles:
        if pdfFile.count("\\") is count_to_verify:
            path_to_verify.append(pdfFile)
    return path_to_verify


def add_reason_to_delete_path(string, data_to_filter, reason_form):
    data_to_erase = data_to_filter[
        data_to_filter["path"].str.contains(string, flags=re.IGNORECASE, regex=True) == True]
    paths = data_to_erase['path'].tolist()
    for path in paths:
        reason_form.append(path, "The file contains " + string + " in the path")



