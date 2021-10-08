import os.path
import unittest
from FilterFileExtract import extract_folder, extract_number_sublevel, extract_files
from ReasonForm import ReasonForm
from xmltojson import extract_parent_parent_directorys
class MyTestCase(unittest.TestCase):
    def test_extract_folder_with_pdf(self):
        url = "\\\\SRV608\\ladossi2020\\NAS"
        xml = ".\\xml_data\\2020\\"
        reason_form = ReasonForm("2020")
        reason_form.compare_folder(url,xml)
        folder_empty = reason_form.get_empty_folders()
        reason_form.extract_empty_folder()
        self.assertEqual(len(folder_empty), 476)


    def test_compare_string(self):
        path_compare = [".\\xml_data\\2020\\NAS\\NAS20-02100 à NAS20-02199\\NAS20-02177     191 chemin Rondeau Saint-Michel-des-Saints\\NAS20-02177     191 chemin Rondeau Saint-Michel-des-Saints_data.xml"]
        parent_parent_directory_name = extract_parent_parent_directorys(path_compare)
        assert parent_parent_directory_name == ["NAS20-02100 à NAS20-02199"]














if __name__ == '__main__':
    unittest.main()
