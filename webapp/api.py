'''
Author: Duc, Sky
Description: 
Date: 2021-02-23 17:41:16
LastEditors: Tianyi Lu
LastEditTime: 2021-03-04 16:56:50
'''
import sys
import flask
import json
import config
import psycopg2
import random

api = flask.Blueprint('api', __name__)

def get_connection():
	'''
	Returns a connection to the database described in the
	config module. May raise an exception as described in the
	documentation for psycopg2.connect.
	'''
	return psycopg2.connect(database=config.database,
							user=config.user,
							password=config.password)

def get_query(query, data=None):
	try:
		connection = get_connection()
		cursor = connection.cursor()
		if (data):
			cursor.execute(query, data)
		else:
			cursor.execute(query)
	except Exception as e:
		print(e, file=sys.stderr)
		exit()
	return cursor

def extend_query(query, conditions):
	if len(conditions) > 0:
		query += " WHERE "
		for i in range(len(conditions)):
			query += conditions[i]
			if i < len(conditions)-1:
				query += " AND "
			else:
				query += " "
	return query

@api.route('/books/search')
# ?title={title}&start_year={start_year}&end_year={end_year}&genres={genres}
# &setting={setting}&character={character}&isbn13={isbn13}
def get_books():
	title = flask.request.args.get('title', default='',type=str)
	start_year = flask.request.args.get('start_year', default=0, type=int)
	end_year = flask.request.args.get('end_year', default=10000, type=int)
	setting = flask.request.args.get('setting', default='', type=str)
	character = flask.request.args.get('character', default='', type=str)
	genres = flask.request.args.get('genres', default='', type=str)
	isbn13 = flask.request.args.get('isbn13', default=0, type=int)

	query = 'SELECT DISTINCT * FROM books, genres, genres_votes'
	query_conditions = []
	query_data = []
	if (title):
		title = "%" + title + "%"
		query_data.append(title)
		query_conditions.append(f"books.title LIKE %s")
	if (start_year):
		query_data.append(start_year)
		query_conditions.append(f"books.date_pubslished > %s")
	if (end_year):
		query_data.append(end_year)
		query_conditions.append(f"books.date_pubslished < %s")
	if (setting):
		setting = "%" + setting + "%"
		query_data.append(setting)
		query_conditions.append(f"books.settings LIKE %s")
	if (character):
		character = "%" + character + "%"
		query_data.append(character)
		query_conditions.append(f"books.characters LIKE %s")
	if (isbn13):
		query_data.append(isbn13)
		query_conditions.append(f"books.isbn13 = %s")
	if len(query_conditions) > 0:
		query = extend_query(query, query_conditions)
	if (genres):
		genres = "%" + genres + "%"
		if len(query_conditions) > 0:
			query += "AND"
		else:
			query += "WHERE"
		query_data.append(genres)
		query += f"genres.genre LIKE %s \
		  AND genres.id = genres_vote.genre_id \
		  AND genres_votes.book_id = book.id"
	query += " ORDER BY books.average_rating LIMIT 10;"
	data = tuple(query_data)
	cursor = get_query(query, data)

	books_list = []

	for row in cursor:
		book_dict = {}
		book_dict['id'] = row[0]
		book_dict['series_id'] = row[1]
		book_dict['title'] = row[2]
		book_dict['cover_link'] = row[3]
		book_dict['rating_count'] = row[4]
		book_dict['average_rate'] = row[5]
		book_dict['review_count'] = row[6]
		book_dict['number_of_page'] = row[7]
		book_dict['date_published'] = row[8]
		book_dict['publisher'] = row[9]
		book_dict['isbn13'] = row[10]
		book_dict['settings'] = row[11]
		book_dict['characters'] = row[12]
		book_dict['amazon_link'] = row[13]
		book_dict['descriptions'] = row[14]
		books_list.append(book_dict)
	return json.dump(books_list)

@api.route('/books/order_by_rating') 
def get_book_by_rating():
	query_head = "SELECT * FROM books" 
	query_tail = "ORDER BY books.average_rate DESC LIMIT 5" 
	query_head = extend_query(query_head, ["books.rating_count > 100"])
	query = query_head + query_tail
	cursor = get_query(query)

	books_list = []

	for row in cursor:
		book_dict = {}
		book_dict['id'] = row[0]
		book_dict['title'] = row[1]
		book_dict['cover_link'] = row[2]
		book_dict['series_id'] = row[3]
		book_dict['rating_count'] = row[4]
		book_dict['review_count'] = row[5]
		book_dict['average_rate'] = row[6]
		book_dict['number_of_page'] = row[7]
		book_dict['date_published'] = row[8]
		book_dict['publisher'] = row[9]
		book_dict['isbn13'] = row[10]
		book_dict['settings'] = row[11]
		book_dict['characters'] = row[12]
		book_dict['amazon_link'] = row[13]
		book_dict['descriptions'] = row[14]
		books_list.append(book_dict)
	return json.dumps(books_list)

@api.route('/books/order_by_date') 
def get_book_by_date():
	query_head = "SELECT * FROM books"
	query_tail = "ORDER BY books.date_published DESC LIMIT 5" 
	query_head = extend_query(query_head, ["books.date_published IS NOT NULL",
								           "LENGTH(books.date_published) = 10",
										   "books.date_published LIKE '2020%'"])
	query = query_head + query_tail
	cursor = get_query(query)

	books_list = []

	for row in cursor:
		book_dict = {}
		book_dict['id'] = row[0]
		book_dict['series_id'] = row[1]
		book_dict['title'] = row[2]
		book_dict['cover_link'] = row[3]
		book_dict['rating_count'] = row[4]
		book_dict['average_rate'] = row[5]
		book_dict['review_count'] = row[6]
		book_dict['number_of_page'] = row[7]
		book_dict['date_published'] = row[8]
		book_dict['publisher'] = row[9]
		book_dict['isbn13'] = row[10]
		book_dict['settings'] = row[11]
		book_dict['characters'] = row[12]
		book_dict['amazon_link'] = row[13]
		book_dict['descriptions'] = row[14]
		books_list.append(book_dict)
	return json.dumps(books_list)

@api.route('/books') 
def get_book_random():
	query = f"SELECT * FROM books ORDER BY RANDOM() LIMIT 4" 
	cursor = get_query(query)

	books_list = []

	for row in cursor:
		book_dict = {}
		book_dict['id'] = row[0]
		book_dict['series_id'] = row[1]
		book_dict['title'] = row[2]
		book_dict['cover_link'] = row[3]
		book_dict['rating_count'] = row[4]
		book_dict['average_rate'] = row[5]
		book_dict['review_count'] = row[6]
		book_dict['number_of_page'] = row[7]
		book_dict['date_published'] = row[8]
		book_dict['publisher'] = row[9]
		book_dict['isbn13'] = row[10]
		book_dict['settings'] = row[11]
		book_dict['characters'] = row[12]
		book_dict['amazon_link'] = row[13]
		book_dict['descriptions'] = row[14]
		books_list.append(book_dict)
	return json.dump(books_list)

@api.route('/books/<book_id>') 
def get_book_by_id(book_id):
	query = f"SELECT * FROM books WHERE books.id = %s" 
	data = (book_id, )
	cursor = get_query(query, data).fetchone()

	books_list = []

	for row in cursor:
		book_dict = {}
		book_dict['id'] = row[0]
		book_dict['series_id'] = row[1]
		book_dict['title'] = row[2]
		book_dict['cover_link'] = row[3]
		book_dict['rating_count'] = row[4]
		book_dict['average_rate'] = row[5]
		book_dict['review_count'] = row[6]
		book_dict['number_of_page'] = row[7]
		book_dict['date_published'] = row[8]
		book_dict['publisher'] = row[9]
		book_dict['isbn13'] = row[10]
		book_dict['settings'] = row[11]
		book_dict['characters'] = row[12]
		book_dict['amazon_link'] = row[13]
		book_dict['descriptions'] = row[14]
		books_list.append(book_dict)
	return json.dump(books_list)

@api.route('/books/recommendation/<book_id>') 
def get_recommendation_by_id(book_id):
	query = f"SELECT * FROM recommendations WHERE recommendations.current_book_id = %s;"
	data = (book_id, ) 
	cursor = get_query(query, data)
	recommendation_dict = {}
	recommendation = cursor[1].split(',')
	recommendation_dict['recommendations'] = recommendation
	return json.dumps(recommendation_dict)

@api.route('/books/genre/<book_id>') 
def get_genre_by_id(book_id):
	query = f"SELECT DISTINCT genre, vote FROM books, genres, genres_votes \
	WHERE genres_votes.book_id = %s \
	AND genres.id = genres_vote.genre_id;"
	data = (book_id, ) 
	cursor = get_query(query, data)
	genres_list = []

	for row in cursor:
		genre_dict = {}
		genre_dict['genre_name'] = cursor[0]
		genre_dict['vote'] = cursor[1]
		genres_list.append(genre_dict)
	return json.dumps(genre_dict)

@api.route('authors/<author_id>') 
def get_author_by_id(author_id):
	query = f"SELECT full_name, birth_place, genre, book_id FROM authors, authors_books WHERE authors.id = %s \
	AND authors_books.id = %s" 
	data = (author_id, author_id) 
	cursor = get_query(query, data)
	author_dict = {}
	books_list = []
	for row in cursor:
		books_list.append(row[3])
	author_dict['name'] = cursor[0][0]
	author_dict['birth_place'] = cursor[0][1]
	author_dict['genre'] = cursor[0][2]
	author_dict['book_id'] = books_list
	return json.dumps(author_dict)

@api.route('authors/search') 
def get_author_by_name(author_id):
	name = flask.request.args.get('name', default='',type=str)
	name = '%' + name + '%'
	data = (name, )
	query = f"SELECT * FROM authors, authors_books WHERE authors.name LIKE %s;"
	cursor = get_query(query, data)
	author_list = []
	for row in cursor:
		author_dict = {}
		author_dict['name'] = cursor[0]
		author_dict['birth_place'] = cursor[1]
		author_dict['genre'] = cursor[2]
		author_list.append(author_dict)
	return json.dumps(author_list)