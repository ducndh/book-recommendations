'''
Author: Duc, Sky
Description: 
Date: 2021-02-19 20:53:27
LastEditors: Tianyi Lu
LastEditTime: 2021-03-06 03:49:41
'''
import sys
import argparse
import flask
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

# This route delivers the user your site's home page.
@app.route('/')
def home():
    return flask.render_template('index.html')

# This route supports relative links among your web pages, assuming those pages
# are stored in the templates/ directory or one of its descendant directories,
# without requiring you to have specific routes for each page.

@app.route('/test')
def book():
    return flask.render_template('test.html')

@app.route('/pending/<path:path>')
def pending(path):
    return flask.render_template('pending.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tiny Flask application, including API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)