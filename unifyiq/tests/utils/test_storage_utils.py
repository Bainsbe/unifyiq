import json
import unittest

from utils.storage.local_file_system import LocalFileSystemStorage


class TestLocalStorageUtils(unittest.TestCase):

    def setUp(self):
        self.localInstance = LocalFileSystemStorage()
        self.obj = json.dumps({
            "name": "John Doe",
            "age": 30,
            "isMarried": True,
            "spouse": {
                "name": "Jane Doe",
                "age": 28,
                "isMarried": True
            }
        })

        self.obj2 = json.dumps({
            "name": "Bobby Doe",
            "age": 28,
            "isMarried": False,
            "spouse": {
                "name": "Jane Doe",
                "age": 28,
                "isMarried": True
            }
        })

        self.test_basic_file = "/tmp/test.txt"
        self.test_multi_file1 = "/tmp/test1.txt"
        self.test_multi_file2 = "/tmp/test2.txt"
        self.test_read_files = "/tmp/read_files_test.txt"
        self.test_full_behaviour_file = "/tmp/full_behaviour_test.txt"

    def test_basic(self):
        self.localInstance.write_line(self.test_basic_file, self.obj)
        self.localInstance.write_line(self.test_basic_file, self.obj2)
        self.localInstance.close_all_write_files()

        read_data = self.localInstance.read_file(self.test_basic_file)[0]
        self.assertEqual(read_data, self.obj)
        read_data = self.localInstance.read_file(self.test_basic_file)[1]

        self.assertEqual(read_data, self.obj2)

    def test_multi_file(self):
        self.localInstance.write_line(self.test_multi_file1, self.obj)
        self.localInstance.write_line(self.test_multi_file2, self.obj2)
        self.localInstance.close_all_write_files()

        read_data_from_test1 = self.localInstance.read_file(self.test_multi_file1)[0]
        read_data_from_test2 = self.localInstance.read_file(self.test_multi_file2)[0]

        self.assertEqual(read_data_from_test1, self.obj)
        self.assertEqual(read_data_from_test2, self.obj2)

    def test_read_files_basic(self):
        self.localInstance.write_line(self.test_read_files, self.obj)
        self.localInstance.write_line(self.test_read_files, self.obj2)
        self.localInstance.close_all_write_files()

        files = self.localInstance.read_file(self.test_read_files)
        self.assertEqual(files[0], self.obj)
        self.assertEqual(files[1], self.obj2)

    def test_full_behaviour(self):
        self.localInstance.write_line(self.test_full_behaviour_file, 'hello')
        self.localInstance.write_line(self.test_full_behaviour_file, 'world')
        self.localInstance.write_line(self.test_full_behaviour_file, 'hello1')
        self.localInstance.write_line(self.test_full_behaviour_file, 'world1')

        self.localInstance.close_all_write_files()

        self.assertEqual(self.localInstance.read_file(self.test_full_behaviour_file),
                         ['hello', 'world', 'hello1', 'world1'])


if __name__ == '__main__':
    unittest.main()
