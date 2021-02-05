'''
Author: Tianyi Lu
Description: Olympics API
Date: 2021-02-05 13:49:43
LastEditors: Tianyi Lu
LastEditTime: 2021-02-05 16:12:49
'''

import flask
import sys
import argparse
import json
from olympics import Olympics

app = flask.Flask(__name__)
olympics_object = Olympics()

@app.route('/')
def hello():
    return 'Hello, this is Olympics API implemented by Sky Lu.'

@app.route('/games')
def games():
    games_list = olympics_object.get_games()
    key_list = ['id', 'year', 'season', 'city']
    result_list = list_to_dict(key_list, games_list)
    return json.dumps(result_list)

@app.route('/nocs')
def nocs():
    nocs_list = olympics_object.get_nocs()
    key_list = ['abbreviation','name']
    result_list = list_to_dict(key_list, nocs_list)
    return json.dumps(result_list)

@app.route('/medalists/games/<games_id>')
def medalists(games_id):
    noc = flask.request.args.get('noc') or None
    key_list = ['athlete_id', 'athlete_name', 'athlete_sex',
                'sport', 'event', 'medal']
    medalists_list = olympics_object.get_medalists_by_games(games_id, noc)
    result_list = list_to_dict(key_list, medalists_list)
    return json.dumps(result_list)

def list_to_dict(key_list, value_list):
    return [{x[0]:x[1] for x in zip(key_list, row)} for row in value_list]

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)