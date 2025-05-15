import unittest
import os
from app import create_app
app = create_app()

class TestUnitLogic(unittest.TestCase):
    def setUp(self):
        self.test_file = 'testdata.txt'
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("ID\tName\tAge\n1\tAlice\t30\n2\tBob\t\n3\t\t25\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_get_new_id_returns_max_plus_one(self):
        self.assertEqual(get_new_id("1"), 2)
        self.assertEqual(get_new_id("5"), 6)

    def test_get_new_id_with_empty(self):
        self.assertEqual(get_new_id(""), 1)

    def test_empty_cells_in_each_column(self):
        with open(self.test_file) as f:
            lines = f.readlines()
        counts = [0] * len(lines[0].strip().split("\t"))
        for line in lines[1:]:
            for i, col in enumerate(line.strip().split("\t")):
                if col == "":
                    counts[i] += 1
        self.assertEqual(counts, [0, 1, 1])

    def test_id_column_update(self):
        from app import fix_empty_ids
        fix_empty_ids(self.test_file)
        with open(self.test_file) as f:
            lines = f.readlines()
        ids = [line.split('\t')[0] for line in lines[1:]]
        self.assertEqual(ids, ['1', '2', '3'])

    def test_windows_to_unix_conversion(self):
        content = "Name\r\nAge\r\n"
        with open(self.test_file, 'wb') as f:
            f.write(content.encode('utf-8'))
        from app import convert_crlf_to_lf
        convert_crlf_to_lf(self.test_file)
        with open(self.test_file, 'rb') as f:
            result = f.read()
        self.assertNotIn(b'\r\n', result)

if __name__ == '__main__':
    unittest.main()
