import unittest

from utils import text_utils


class TestTextUtil(unittest.TestCase):
    def test_normalize(self):
        res = text_utils.normalize(" Hello\nWorld ")
        exp = "Hello World"
        self.assertEqual(res, exp)

    def test_add_space_if_not_empty(self):
        res = text_utils.add_space_if_not_empty("Hello")
        exp = "Hello "
        self.assertEqual(res, exp)
        res = text_utils.add_space_if_not_empty("")
        exp = ""
        self.assertEqual(res, exp)


if __name__ == '__main__':
    unittest.main()
