
'''
Author: Kyosuke Imai, Kevin Phung
Date: 2/19/21
'''

import argparse
import sys
import flask
import json
import psycopg2
import datetime

# Please create your config file
from config import password
from config import database
from config import user


app = flask.Flask(__name__)


def connection_to_database():
    '''
    Return a connection object to the postgres database
    '''
    try:
        connection = psycopg2.connect(database = database, user= user, password = password)
        return connection
    except Exception as e:
        print(e)
        exit()

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

def get_homepage_query():
    '''
    Placeholder
    '''
    query = "get home page info\
        "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/home')
def get_songs():
    pass
    return json.dumps(top_20_songs_list)

def get_search_results():
    category_to_search_by = flask.request.args.get('category_to_search_by')
    category_to_search_for = flask.request.args.get('category_to_search_for')
    result_size= flask.request.args.get('result_size')
    search_string= flask.request.args.get('search_string')

    if search_string==None:
        raise ValueError('search parameter cannot be empty')

    if !(search_string.isascii()):
        raise TypeError('Search string must be ascii char')

    if len(search_string)>= 100 :
        raise ValueError('search parameter is greater than 100 characters')

    query = "\
    get songs info based on search query\
    "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/search/category_to_search_by={category}&category_to_search_for={category}&result_size={chosen result size per page}&search_string=(user search string)')
def get_results():
    pass
    return json.dumps(results_list)


def get_all_playlists():
    query = "\
    Get all playlists from storage\
    "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/your_playlists')
def get_list_of_playlists():
    pass
    return json.dumps(playlists_list)


def get_specific_playlist():
    query = "\
    Get specific playlist details from storage\
    "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/playlist_name={actual playlist name}')
def get_playlist_details():
    pass
    return json.dumps(playlist_songs)





if __name__ == '__main__':
    parser = argparse.ArgumentParser('An API to retrieve data from the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)





# class SearchStringChecker:
#     def __init__(self, search_string):
#         self.search_string = search_string
#
#
#     def get_search_string(self):
#         return self.search_string
#
    # def is_not_empty(self):
    #     if self.search_string==None:
    #         raise ValueError('search parameter cannot be empty')
#
#         return True
#
    # def string_is_ascii(self):
    #     if (self.search_string.isascii()):
#             return True
#
#         else:
#             return False
#
#     def is_too_long(self,n):
        # if len(self.search_string)>= n :
        #     raise ValueError('search parameter is greater than %n characters')
#
#         return False
