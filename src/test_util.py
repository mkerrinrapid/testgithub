import unittest

import util

class TestUtil(unittest.TestCase):

    def test_calc(self):
        assert True

    def test_erh(self):
        assert True

    def test_erh2(self):
        assert True

    def test_erh3(self):
        assert True

    def test_calc_issues(self):
        result =  util.calc_something(2, 4)
        assert result == 8
