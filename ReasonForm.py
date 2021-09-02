import pandas as pd

class ReasonForm:
    def __init__(self):
        self.reasons =[]
        self.paths = []

    def append(self, path_to_append, reason_to_append):
        self.reasons.append(reason_to_append)
        self.paths.append(path_to_append)

    def extract_to_pdf(self):
        reason_and_path = {'Paths': self.paths, 'Reasons_why_is_not_in_xml': self.reasons}
        reason_and_path_dataframe = pd.DataFrame(reason_and_path)
        reason_and_path_dataframe.to_csv(".\\pdf_that_are_not_extract.csv")

    def get_reasons(self):
        return self.reasons

    def get_paths(self):
        return self.paths
