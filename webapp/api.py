'''
Author: Duc, Sky
Description: 
Date: 2021-02-23 17:41:16
LastEditors: Tianyi Lu
LastEditTime: 2021-02-23 22:01:26
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

@api.route('/books') 
def get_books():
    # Of course, your API will be extracting data from your postgresql database.
    # To keep the structure of this tiny API crystal-clear, I'm just hard-coding data here.
    connection = None
    try:
        connection = psycopg2.connect(database=config.database,
                                      user=config.user,
                                      password=config.password)
    except Exception as e:
        print(e)
        exit(0)

    cursor = connection.cursor()
    query = 'SELECT * FROM books;'
    cursor.execute(query)
    
    book_lists = []
    for row in cursor:
        if (len(book_lists) >= 10):
            break;

        if (row[10]):
            characters = [x.strip() for x in row[10].split(',')]
        else:
            characters = []

        book_dict = {'id': int(row[0]),
                     'title': row[1],
                     'cover_link': row[2],
                     'rating_count': int(row[3]),
                     'review_count': int(row[4]),
                     'number_of_page': int(row[5]),
                     'date_published': row[6],
                     'publisher': row[7],
                     'isbn13': row[8],
                     'settings': row[9],
                     'characters': characters,
                     'amazon_link': row[11],
                     'description': row[12] or '(No Description)'}
        book_lists.append(book_dict)

    return json.dumps(book_lists)

@api.route('/books/<id>') 
def get_dogs():
    dogs = [{'name':'Ruby', 'birth_year':2003, 'death_year':2016, 'description':'a very good dog'},
            {'name':'Maisie', 'birth_year':2017, 'death_year':None, 'description':'a very good dog'}]
    return json.dumps(dogs)