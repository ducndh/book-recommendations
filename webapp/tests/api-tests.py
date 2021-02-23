'''
Author: Duc, Sky
Description: 
Date: 2021-02-19 20:03:49
LastEditors: Tianyi Lu
LastEditTime: 2021-02-23 22:40:35
'''

import unittest
import requests

class WebappApiTester(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000"
        try:
            requests.get(self.url)
        except Exception as e:
            print(e)
        
    def test_get_book_by_correct_id(self):
        correct_json = {'title': 'Macbeth',
                        'series_name': '',
                        'description': '',
                        'cover_link': ''} # We will fill this out after database is populated
        api_url = '/'.join(self.url, 'books', 20)
        r = requests.get(api_url)
        self.assertEqual(correct_json, r.json())

    def test_get_book_by_out_of_range_id(self):
        api_url1 = '/'.join(self.url, 'books', -1)
        api_url2 = '/'.join(self.url, 'books', 2,147,483,647)
        r1 = requests.get(api_url1)
        r2 = requests.get(api_url2)
        self.assertIs((r1 or r2), None)

    
    def test_search_books(self):
        api_url = '/'.join(self.url, 'books', 'search')
        r = requests.get(api_url, params={'title': 'world',
                                          'genre': 'fiction',
                                          'data': '1800-01-01'})
        correct_json = [{'title': 'Hello World',}] # We will fill this out after database is populated
        self.assertCountEqual(r.json(), correct_json)
    
    def test_search_books_empty(self):
        api_url = '/'.join(self.url, 'books', 'search')
        r = requests.get(api_url)
        self.assertEqual(len(r.json()), 0)

    def test_get_reviews(self):
        api_url = '/'.join(self.url, 'books', 'reviews', 10)
        r = requests.get(api_url)
        correct_json = [{'user_id': 62, 'content': 'this is a good book'},] # We will fill this out after database is populated
        self.assertCountEqual(correct_json, r.json())

    def test_get_ratings(self):
        api_url = '/'.join(self.url, 'books', 'ratings', 12)
        r = requests.get(api_url)
        correct_json = [{'one_star_rating': 345}]  #We will fill this out after database is populated
        self.assertCountEqual(correct_json, r.json())

    def test_get_book_recommendation(self):
        correct_json = {'recommendations': [2194412, 42141, 1214124, 52342342, 893424321]}
        api_url = '/'.join(self.url, 'books', 'recommendation', 3424234)
        r = requests.get(api_url)
        self.assertCountEqual(correct_json, r.json())

    def test_get_book_genre(self):
        correct_json = [{'genre_name': 'sci-fi', 'vote': 179}, {'genre_name': 'horror', 'vote': 32}]
        api_url = '/'.join(self.url, 'books', 'genre', 3424234)
        r = requests.get(api_url)
        self.assertCountEqual(correct_json, r.json())

    def get_author_by_id(self):
        correct_json = {'name':"Shakespeare", 'birth_place': "England", 'genre': "tragedies, comedies, history"}
        api_url = '/'.join(self.url, 'authors', 3232)
        r = requests.get(api_url)
        self.assertEqual(correct_json, r.json())

    def get_author_by_name(self):
        correct_json = [{'name':"Nam Cao", 'birth_place': "Viet Nam", 'genre': "tragedies, histories"}, {'name': "Cao Ling", 'birth_place':"China", 'genre': "fantasy, adventure, romance"}]
        api_url = '/'.join(self.url, 'authors', 'search')
        r = requests.get(api_url, params={'name': 'Cao'})
        self.assertCountEqual(correct_json, r.json())
        
    def get_author_by_name_empty(self):
        correct_json = []
        api_url = '/'.join(self.url, 'authors', 'search')
        r = requests.get(api_url, params={'name': 162348761234})
        self.assertCountEqual(correct_json, r.json())

    def test_get_bookshelf(self):
        correct_json = {'books_id': [841292134, 92141234, 23493214]}
        api_url = '/'.join(self.url, 'user' , 'bookshelf')
        r = requests.get(api_url)
        self.assertEqual(correct_json, r.json())





