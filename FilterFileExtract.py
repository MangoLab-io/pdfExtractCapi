import os
import time
import re
import pandas as pd
import logging

logging.basicConfig(filename='information_with_path_data.log', level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def get_last_or_second_last_modify_file(all_path_to_analyse, reason_form):
    array_path = []
    for path in all_path_to_analyse:
        fileStatsObj = os.stat(path)
        modificationTime = time.ctime(fileStatsObj.st_mtime)
        array_path.append([os.path.dirname(path), path, modificationTime])
    data_to_filter = pd.DataFrame(array_path, columns=['directory', 'path', 'time_modify'])
    data_to_filter['time_modify'] = pd.to_datetime(data_to_filter['time_modify'])
    data_to_filter.sort_values(by=['directory', 'time_modify'], inplace=True, ascending=[True, False])
    data_to_filter = data_to_filter.groupby(by='directory').head(2)
    remove_string_in_path =['invoice','honos', 'demande originale', 'scan','facture', 'Demandes annulées', 'permis', 'plan']
    for string in remove_string_in_path:
        add_reason_to_delete_path(string, data_to_filter, reason_form)
        data_to_filter = data_to_filter[
            data_to_filter['path'].str.contains(string, flags=re.IGNORECASE, regex=True) == False]

    return data_to_filter['path'].tolist()


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


def extract_folder(path):
    # the path should be absolut
    try:
        folder = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for directory in d:
                full_path = os.path.join(r, directory)
                folder.append(full_path)

        return folder
    except:
        print("Somethings went wrong with extract folder")


def extract_files(path, extension):
    # the path should be absoluth
    try:
        xml_Files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith(extension):
                    full_path = os.path.join(r, file)
                    xml_Files.append(full_path)

        return xml_Files
    except:
        print("Somethings went wrong while extracting file")
        logging.info(f'Somethings went wrong while extracting files')


