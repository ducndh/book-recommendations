'''
Author: Duc, Sky
Description: Converting goodreads.csv to small csvs we need.
Date: 2021-02-23 18:23:11
LastEditors: Tianyi Lu
LastEditTime: 2021-03-04 16:14:49
'''
import csv
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
columns = {'id': 0, 'title': 1, 'link': 2, 'series': 3, 'cover_link': 4,
           'author': 5, 'author_link': 6, 'rating_count': 7, 'review_count': 8,
           'average_rating': 9, 'five_star_ratings': 10, 'four_star_ratings': 11,
           'three_star_ratings': 12, 'two_star_ratings': 13, 'one_star_ratings': 14,
           'number_of_pages': 15, 'date_published': 16, 'publisher': 17,
           'original_title': 18, 'genre_and_votes': 19, 'isbn': 20, 'isbn13': 21,
           'asin': 22, 'settings': 23, 'characters': 24, 'awards': 25, 
           'amazon_redirect_link': 26, 'recommended_books': 28, 'description': 30,}

def read_csv(filename):

    rows = []
    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row[3] = series_extracter(row[3])
                row[16] = date_converter(row[16].split())
                rows.append(row)

    except Exception as e:
        print(e)
    
    return rows[1:]

def write_from_goodreads(filename, rows_input, column_names = [], convert_names = [], generate_id = False):
    total_row = 0
    if len(column_names) == 0:
        raise RuntimeError('Error [write_from_goodreads]: column_names cannot be empty.')

    
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        seen_set = set()
        for row in rows_input:
            
            row_content_list = []
            for name in column_names:
                row_content = row[columns[name]]
                if name in convert_names:
                    row_content = get_id_from_file(name+'.csv', row_content)
                row_content_list.append(row_content)

            if len(row_content_list) == 0 or row_content_list[0] == None:
                continue

            row_content = tuple(row_content_list)
            if row_content not in seen_set:
                seen_set.add(row_content)
                if generate_id:
                    row_content_list.insert(0, len(seen_set))
                csv_writer.writerow(row_content_list)
                total_row += 1
                print(total_row)

def write_books_authors(rows_input):
    total_row = 0
    with open(parent_dir + '/static/books_authors.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows_input:
            book_id = row[0]
            author_ids = [get_id_from_file('authors.csv', x.strip()) for x in row[5].split(',')]
            for author_id in author_ids:
                if author_id == None:
                    continue
                csv_writer.writerow([book_id, author_id])
                total_row += 1
                print(total_row)

def write_genres(rows_input):
    total_row = 0
    with open(parent_dir + '/static/genres.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        seen_genre = set()
        for row in rows_input:
            genres_votes = [x.strip() for x in row[19].split(',')]
            if len(genres_votes) <= 1:
                continue
            for genre_vote in genres_votes:
                *genre, vote = genre_vote.split()
                genre = ' '.join(genre)
                if genre not in seen_genre:
                    seen_genre.add(genre)
                    csv_writer.writerow([len(seen_genre), genre])
            total_row += 1
            print(total_row)

def write_genres_votes(rows_input):
    total_row = 0
    with open(parent_dir + '/static/genres_votes.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows_input:
            book_id = row[0]
            genres_votes = [x.strip() for x in row[19].split(',')]
            if len(genres_votes) <= 1:
                continue
            for genre_vote in genres_votes:
                *genre, vote = genre_vote.split()
                vote = vote.replace("user", "")
                genre = ' '.join(genre)
                genre_id = get_id_from_file('genres.csv', genre)
                csv_writer.writerow([book_id, genre_id, vote])
            total_row += 1
            print(total_row)

def write_awards(rows_input):
    total_row = 0
    with open(parent_dir + '/static/awards.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        seen_awards = set()
        for row in rows_input:
            awards_years = [x.strip() for x in row[25].split(',')]
            if len(awards_years) <= 1:
                continue
            for award_year in awards_years:
                *award, year = award_year.split()
                award = ' '.join(award)
                if award not in seen_awards:
                    seen_awards.add(award)
                    csv_writer.writerow([len(seen_awards), award])
            total_row += 1
            print(total_row)

def write_books_awards(rows_input):
    total_row = 0
    with open(parent_dir + '/static/books_awards.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows_input:
            book_id = row[0]
            book_awards = [x.strip() for x in row[25].split(',')]
            if len(book_awards) <= 1:
                continue
            for book_award in book_awards:
                *award, year = book_award.split()
                award = ' '.join(award)
                year = year.strip('()')
                try:
                    year = int(year)
                except:
                    year = ''

                award_id = get_id_from_file('awards.csv', award)
                csv_writer.writerow([book_id, award_id, year])
            total_row += 1
            print(total_row)

def write_recommendations(rows_input):
    total_row = 0
    with open(parent_dir + '/static/recommendations.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows_input:
            total_row += 1
            print(total_row)
            book_id = row[0]
            recommendations = [x.strip() for x in row[28].split(',')]
            if len(recommendations) <= 1:
                continue
            for recommendation in recommendations:
                try:
                    recommendation = int(recommendation)
                except:
                    continue

                csv_writer.writerow([book_id, recommendation])

def get_id_from_file(filename, keyword):
    with open(parent_dir + '/static/' + filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if keyword in row:
                return row[0]

        return None

def series_extracter(raw_input):
    # raw form: "(Private #5)"
    if raw_input:
        return ' '.join(raw_input.strip('()').split()[:-1])
    else:
        return None

def date_converter(date_list):
    if (len(date_list) == 0):
        return ''
    elif (len(date_list) == 1):
        return '-'.join([date_list[0], '01', '01'])
    elif (len(date_list) == 3):
        return '-'.join([date_list[2], 
                         map_month_to_number(date_list[0]), 
                         map_date_to_number(date_list[1])])  
    else:
        return ''

def map_month_to_number(input_string):
    month_dict = {'january': '01',
                  'februrary': '02',
                  'march': '03',
                  'april': '04',
                  'may': '05',
                  'june': '06',
                  'july': '07',
                  'august': '08',
                  'september': '09',
                  'october': '10',
                  'november': '11',
                  'december': '12'}

    return month_dict.get(input_string.lower(), '01')

def map_date_to_number(input_string):
    number = input_string[:-2]
    return '0'+number if len(number) == 1 else number


if __name__ == "__main__":
    goodreads_rows = read_csv(parent_dir + '/static/goodreads_books.csv')
    
    try:
        # write_from_goodreads(parent_dir + '/static/series.csv', goodreads_rows, 
        #                      column_names = ['series'], generate_id=True)

        # write_from_goodreads(parent_dir + '/static/books.csv', goodreads_rows,
        #                      column_names = ['id', 'title', 'cover_link', 'series', 
        #                                      'rating_count', 'review_count', 
        #                                      'average_rating', 'number_of_pages',
        #                                      'date_published', 'publisher', 'isbn13', 
        #                                      'settings', 'characters', 'amazon_redirect_link',
        #                                      'description'],
        #                      convert_names = ['series'])
        # write_books_authors(goodreads_rows)
        # write_genres(goodreads_rows)
        # write_genres_votes(goodreads_rows)
        # write_awards(goodreads_rows)
        # write_books_awards(goodreads_rows)
        write_recommendations(goodreads_rows)
    except Exception as e:
        print('Error: '+str(e))
        exit(0)