'''
Author: Tianyi Lu
Description: Postgresql command-line interface
Date: 2021-01-29 18:05:08
LastEditors: Tianyi Lu
LastEditTime: 2021-02-05 21:00:26
'''
import psycopg2
import argparse

class Olympics(object):
    def __init__(self):
        self.__connection = self.__get_connection('olympics','','')

        self.__cursor = self.__get_cursor()

    def __del__(self):
        self.__connection.close() # Close the connection to psql when function ends
        
    def __get_connection(self, database, user, password):
        try:
            connection = psycopg2.connect(database=database, 
                                          user=user, 
                                          password=password)
        except Exception as e:
            print(e)
            exit()

        return connection

    def __get_cursor(self):
        try:
            cursor = self.__connection.cursor()
        except Exception as e:
            print(e)
            exit()

        return cursor

    def __get_item_list(self, query):
        self.__cursor.execute(query)
        return [row for row in self.__cursor]

    def get_games(self):
        query = '''
                SELECT DISTINCT games.id, games.game_year, games.season, cities.city_name
                FROM games, cities, games_cities
                WHERE games.id = games_cities.game_id
                AND cities.id = games_cities.city_id
                ORDER BY games.game_year;
                '''
        return self.__get_item_list(query)

    def get_nocs(self):
        query = '''
                SELECT DISTINCT nocs.noc_name, nocs.region
                FROM nocs
                ORDER BY nocs.noc_name;
                '''
        return self.__get_item_list(query)

    def get_medalists_by_games(self, game_id, noc=None):
        query = f'''
                 SELECT DISTINCT athletes.id, athletes.full_name, athletes.sex, 
                 events.event_name, medals.medal
                 FROM athletes, events, medals, games
                 WHERE athletes.id = medals.athlete_id
                 AND events.id = medals.event_id
                 AND games.id = medals.game_id
                 AND medals.medal IS NOT NULL
                 AND games.id = {game_id}
                 ORDER BY athletes.full_name;
                 '''
        query_with_noc = f'''
                          SELECT DISTINCT athletes.id, athletes.full_name, athletes.sex, 
                          events.event_name, medals.medal
                          FROM athletes, events, medals, games, athletes_nocs, nocs
                          WHERE athletes.id = medals.athlete_id
                          AND events.id = medals.event_id
                          AND games.id = medals.game_id
                          AND athletes.id = athletes_nocs.athlete_id
                          AND nocs.id = athletes_nocs.noc_id
                          AND medals.medal IS NOT NULL
                          AND games.id = {game_id}
                          AND nocs.noc_name = '{noc}'
                          ORDER BY athletes.full_name;
                          '''

        return self.__get_item_list((query_with_noc if noc else query))
