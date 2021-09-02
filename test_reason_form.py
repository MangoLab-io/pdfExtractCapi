import unittest
from ReasonForm import ReasonForm

class MyTestCase(unittest.TestCase):
    def test_(self):
        reason_form = ReasonForm()
        reason_form.append("path1", "reason1")
        reason_form.append("path2", "reason2")
        self.assertEqual(reason_form.get_reasons(), ["reason1","reason2"])
        self.assertEqual(reason_form.get_paths(), ["path1", "path2"])



if __name__ == '__main__':
    unittest.main()
