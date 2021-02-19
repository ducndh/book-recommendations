'''
Author: Tianyi Lu
Description: 
Date: 2021-02-19 20:57:51
LastEditors: Tianyi Lu
LastEditTime: 2021-02-19 21:07:54
'''

import unittest
import requests

class OlympicsTester(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000/"
        try:
            r = requests.get(url)
        except:
            print("Connection Failed")
    def test_a(self):
        r = requests.get(self.url+"nocs")
        dic = r.json()
        print(dic)

if __name__ == '__main__':
    unittest.main()
        