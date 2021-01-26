'''
Author: Aiden, Sky
Description: COnverting original csv files
Date: 2021-01-26 18:36:06
LastEditors: Tianyi Lu
LastEditTime: 2021-01-26 19:58:06
'''

import csv

def read_athlete_events():
    """
    Load books from books.csv
    :return: A list of book objects
    """
    with open('athlete_events.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row

def write_from_athlete_events(filename, position_list):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_iter = read_athlete_events()
        next(csv_iter)
        exist_rows = []
        for i, row in enumerate(csv_iter):
            row_content = [row[x] for x in position_list]
            if row_content not in exist_rows:
                csv_writer.writerow([len(exist_rows)]+row_content)
                exist_rows.append(row_content)

def write_athletes_csv():
    write_from_athlete_events('athletes.csv', [1,2,4,5])

def write_games_csv():
    write_from_athlete_events('games.csv', [8,9,10])
    

def write_cities_csv():
    write_from_athlete_events('cities.csv', [11])


if __name__ == "__main__":
    write_athletes_csv()
    # write_games_csv()
    # write_cities_csv()
            
