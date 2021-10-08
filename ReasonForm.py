from FilterFileExtract import extract_files, extract_number_sublevel
import pandas as pd
import os


class ReasonForm:
    def __init__(self, year):
        self.reasons = []
        self.paths = []
        self.folder = []
        self.empty_folders = []
        self.year = year

    def append(self, path_to_append, reason_to_append):
        self.reasons.append(reason_to_append)
        self.paths.append(path_to_append)

    def extract_to_pdf(self):
        reason_and_path = {'Paths': self.paths, 'Reasons_why_is_not_in_xml': self.reasons}
        reason_and_path_dataframe = pd.DataFrame(reason_and_path)
        self.create_folder(".\\logs\\"+self.year)
        reason_and_path_dataframe.to_csv(".\\logs\\"+self.year+"\\pdf_that_are_not_extract.csv")

    def extract_empty_folder(self):
        folder_empty_json = {'empty_folder': self.empty_folders}
        folder_empty_json_dataframe = pd.DataFrame(folder_empty_json)
        self.create_folder(".\\logs\\" + self.year)
        folder_empty_json_dataframe.to_csv(".\\logs\\"+self.year+"\\folder_empty.csv")


    def get_reasons(self):
        return self.reasons

    def get_paths(self):
        return self.paths

    def get_empty_folders(self):
        return self.empty_folders

    def compare_folder(self, path_pdf, path_xml):
        # Regarde les folders qui contiennent des pdfs qui n'ont pas d'extrait
        paths_with_pdf = extract_files(path_pdf, ".pdf")
        paths_with_pdf_sublevel=None
        if path_pdf.endswith("NAS"):
            paths_with_pdf_sublevel = extract_number_sublevel(paths_with_pdf, path_pdf, 3)
        else:
            paths_with_pdf_sublevel = extract_number_sublevel(paths_with_pdf, path_pdf, 2)
        folders = []
        for path_with_pdf in paths_with_pdf_sublevel:
            if os.path.dirname(path_with_pdf) not in folders:
                folders.append(os.path.dirname(path_with_pdf))

        directory_to_split_0 = os.path.split(path_pdf)[1]
        for folder in folders:
            folder_to_add = folder.split(directory_to_split_0 + "\\")[1]
            folder_to_walk = path_xml + directory_to_split_0 + "\\" + folder_to_add
            pdf_file = extract_files(folder_to_walk, ".xml")
            if not pdf_file:
                self.empty_folders.append(folder_to_walk)

    def create_folder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)




