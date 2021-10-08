import unittest
from ReasonForm import ReasonForm

class MyTestCase(unittest.TestCase):
    def test_reason_form_append(self):
        reason_form = ReasonForm()
        reason_form.append("path1", "reason1")
        reason_form.append("path2", "reason2")
        self.assertEqual(reason_form.get_reasons(), ["reason1","reason2"])
        self.assertEqual(reason_form.get_paths(), ["path1", "path2"])

    def test_compare_folder_which_are_not_create_or_are_empty(self):
        url = "C:\Users\dpare\Desktop\data_essai"














if __name__ == '__main__':
    unittest.main()
