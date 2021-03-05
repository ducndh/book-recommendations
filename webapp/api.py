'''
Author: Duc, Sky
Description: 
Date: 2021-02-23 17:41:16
LastEditors: Tianyi Lu
LastEditTime: 2021-03-06 03:10:49
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
	title = flask.request.args.get('title', default=None,type=str)
	# start_year = flask.request.args.get('start_year', default=None, type=int)
	# end_year = flask.request.args.get('end_year', default=None, type=int)
	setting = flask.request.args.get('setting', default=None, type=str)
	character = flask.request.args.get('character', default=None, type=str)
	genres = flask.request.args.get('genres', default=None, type=str)
	isbn13 = flask.request.args.get('isbn13', default=None, type=int)

	query = 'SELECT DISTINCT * FROM books'
	query_conditions = ["books.rating_count > 50"]
	query_data = []
	# if (start_year):
	# 	query_data.append(start_year)
	# 	query_conditions.append(f"books.date_published > %s")
	# if (end_year):
	# 	query_data.append(end_year)
	# 	query_conditions.append(f"books.date_published < %s")
	if (title):
		title = "%" + title.lower() + "%"
		query_data.append(title)
		query_conditions.append(f"LOWER(books.title) LIKE %s")
	if (setting):
		setting = "%" + setting.lower() + "%"
		query_data.append(setting)
		query_conditions.append(f"LOWER(books.settings) LIKE %s")
	if (character):
		character = "%" + character.lower() + "%"
		query_data.append(character)
		query_conditions.append(f"LOWER(books.characters) LIKE %s")
	if (isbn13):
		query_data.append(isbn13)
		query_conditions.append(f"books.isbn13 = %s")
	if (genres):
		query = "SELECT DISTINCT books.id, books.series_id, books.title, books.cover_link, \
			     books.rating_count, books.review_count, books.average_rate, books.number_of_page, \
				 books.date_published, books.publisher, books.isbn13, books.settings, books.characters, \
				 books.amazon_link, books.descriptions \
				 FROM books, genres, genres_votes"
				 
		genres = "%" + genres.lower() + "%"

		query_data.append(genres)
		query_conditions.append(f"LOWER(genres.genre) LIKE %s \
		  AND genres.id = genres_votes.genre_id \
		  AND books.id = genres_votes.book_id")
	
	if len(query_conditions) > 0:
		query = extend_query(query, query_conditions)

	query += " ORDER BY books.average_rate DESC LIMIT 10;"
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

@api.route('/books/order_by_rating') 
def get_book_by_rating():
	query_head = "SELECT * FROM books" 
	query_tail = "ORDER BY books.average_rate DESC LIMIT 10" 
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
		book_dict['description'] = row[14]
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
		book_dict['description'] = row[14]
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
		book_dict['description'] = row[14]
		books_list.append(book_dict)
	return json.dumps(books_list)

@api.route('/books/<book_id>') 
def get_book_by_id(book_id):
	query = f"SELECT * FROM books WHERE books.id = %s" 
	data = (book_id, )
	cursor = get_query(query, data).fetchone()

	book_dict = {}
	book_dict['id'] = cursor[0]
	book_dict['series_id'] = cursor[1]
	book_dict['title'] = cursor[2]
	book_dict['cover_link'] = cursor[3]
	book_dict['rating_count'] = cursor[4]
	book_dict['review_count'] = cursor[5]
	book_dict['average_rate'] = cursor[6]
	book_dict['number_of_page'] = cursor[7]
	book_dict['date_published'] = cursor[8]
	book_dict['publisher'] = cursor[9]
	book_dict['isbn13'] = cursor[10]
	book_dict['settings'] = cursor[11]
	book_dict['characters'] = cursor[12]
	book_dict['amazon_link'] = cursor[13]
	book_dict['descriptions'] = cursor[14]
	return json.dumps(book_dict)

@api.route('/books/recommendation/<book_id>') 
def get_recommendation_by_id(book_id):
	query = f"SELECT recommendations.recommended_book_id \
		      FROM recommendations WHERE recommendations.current_book_id = %s;"
	data = (book_id, ) 
	cursor = get_query(query, data)
	recommendation_dict = {}
	recommendation_dict['recommendations'] = []
	for row in cursor:
		recommendation_dict['recommendations'].append(row[0])
	return json.dumps(recommendation_dict)

@api.route('/books/genre/<book_id>') 
def get_genre_by_id(book_id):
	query = f"SELECT DISTINCT genres.genre, genres_votes.vote FROM books, genres, genres_votes \
	WHERE genres_votes.book_id = %s \
	AND genres.id = genres_votes.genre_id;"
	data = (book_id, ) 
	cursor = get_query(query, data)
	genres_list = []

	for row in cursor:
		genre_dict = {}
		genre_dict['genre_name'] = row[0]
		genre_dict['vote'] = row[1]
		genres_list.append(genre_dict)
	return json.dumps(genres_list)


# full_name text,
#     cover_link text,
#     birth_place text,
#     about text
@api.route('/authors/<author_id>') 
def get_author_by_id(author_id):
	query = f"SELECT DISTINCT authors.full_name, authors.cover_link, \
	          authors.birth_place, authors.about, books_authors.book_id \
		      FROM authors, books_authors WHERE authors.id = %s \
	          AND books_authors.author_id = authors.id;" 
	data = (author_id,) 
	cursor = get_query(query, data)
	author_dict = {}
	books_list = []
	for row in cursor:
		author_dict['full_name'] = row[0]
		author_dict['cover_link'] = row[1]
		author_dict['birth_place'] = row[2]
		author_dict['about'] = row[3]
		books_list.append(row[4])

	author_dict['book_id'] = books_list
	return json.dumps(author_dict)

@api.route('/authors/search') 
def get_author_by_name():
	name = flask.request.args.get('name', default='',type=str)
	name = '%' + name.lower() + '%'
	data = (name, )
	query = f"SELECT * FROM authors WHERE LOWER(authors.full_name) LIKE %s;"
	cursor = get_query(query, data)
	author_list = []
	for row in cursor:
		author_dict = {}
		author_dict['full_name'] = row[0]
		author_dict['cover_link'] = row[1]
		author_dict['birth_place'] = row[2]
		author_dict['about'] = row[3]
		author_list.append(author_dict)
	return json.dumps(author_list)

@api.route('/genres')
def get_genres():
	query = "SELECT genres.genre FROM genres WHERE LENGTH(genres.genre) < 12 AND genres.genre <> 'Pornography' ORDER BY RANDOM() LIMIT 10;"
	cursor = get_query(query, tuple())
	return json.dumps([x[0] for x in cursor])

@api.route('/help')
def get_help():
	with open('doc/api-design.txt', 'w') as f:
		return json.dumps(f)
