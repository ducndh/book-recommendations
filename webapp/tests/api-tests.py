'''
Author: Tianyi Lu
Description: unittest for api
Date: 2021-02-19 20:03:49
LastEditors: Tianyi Lu
LastEditTime: 2021-02-19 21:14:24
'''

import unittest
import requests

class WebappApiTester(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000/"
        try:
            requests.get(self.url)
        except Exception as e:
            print(e)
        
    def test_get_book_by_id(self):
        self.assertEqual