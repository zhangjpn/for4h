# -*- coding:utf-8 -*-

from app.commontools import str_to_date
import unittest


class ToolTestCase(unittest.TestCase):
    def setUp(self):
        self.s = '2017-06-07'
    def tearDown(self):
        self.s = None

    def test_str_to_date(self):
        res = str_to_date(self.s)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()