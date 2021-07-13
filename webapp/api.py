"""authors: Kevin Phung, Kyosuke Imai"""
import sys
import flask
import simplejson as json
from config import *
import psycopg2
import argparse

api = flask.Blueprint('api', __name__)
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

def get_song_by_search():
    '''
    Get a cursor that contains the top 150 songs sorted by popularity and song ID
    Returns:
        cursor: the cursor object with song attributes to iterate over
    '''
    song_name = flask.request.args.get('search')
    song_name = '%' +  song_name + '%'
    query = "\
        SELECT song_details.song_name, STRING_AGG(artist_details.artist_name, ' and '), song_details.release_year, song_details.popularity,\
        song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability, song_details.song_id \
        FROM song_details,song_characteristics,artist_details,song_artist_link \
        WHERE LOWER(song_details.song_name) LIKE LOWER(%s) AND song_details.song_id=song_characteristics.song_id \
        AND artist_details.artist_id=song_artist_link.artist_id AND song_details.song_id= song_artist_link.song_id \
        GROUP BY song_details.song_name,song_details.release_year, song_details.popularity,\
        song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability, song_details.song_id\
        ORDER BY song_details.popularity DESC , song_details.song_id DESC\
        LIMIT 150;"


    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (song_name,))
        print(cursor)
        return cursor
    except Exception as e:
        print(e)
        exit()


def get_song_id_by_artist():
    '''
    Get a cursor that contains the top 150 songs from artists that match the name sorted by popularity and song ID
    Returns:
        cursor: the cursor object with song attributes and artist attributes to iterate over
    '''
    artist_name = flask.request.args.get('search')
    artist_name = '%' +  artist_name + '%'
    query = "\
        With SubQ as (SELECT song_details.song_id, artist_characteristics.tempo, artist_characteristics.duration,\
        artist_characteristics.danceability \
        FROM song_details,artist_details,song_characteristics,artist_characteristics,song_artist_link\
        WHERE LOWER(artist_details.artist_name) LIKE LOWER(%s)\
        AND song_details.song_id = song_characteristics.song_id\
        AND artist_details.artist_id=artist_characteristics.artist_id \
        AND artist_details.artist_id = song_artist_link.artist_id\
        AND song_details.song_id = song_artist_link.song_id\
        ORDER BY song_details.song_id ASC\
        LIMIT 150)\
        SELECT song_details.song_name,STRING_AGG(artist_details.artist_name, ' and '), song_details.release_year, song_details.popularity,\
            song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability, song_details.song_id, SubQ.tempo, SubQ.duration, SubQ.danceability \
            FROM song_details,song_characteristics,artist_details,song_artist_link,SubQ \
            WHERE song_details.song_id = SubQ.song_id AND song_details.song_id=song_characteristics.song_id \
            AND artist_details.artist_id=song_artist_link.artist_id AND song_details.song_id= song_artist_link.song_id \
	    GROUP BY song_details.song_name, song_details.release_year, song_details.popularity,\
            song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability, song_details.song_id, SubQ.tempo, SubQ.duration, SubQ.danceability \
            ORDER BY popularity DESC, song_details.song_id DESC\
            LIMIT 150;"

    connection = connection_to_database()
    try:
        cursor_for_ids = connection.cursor()
        cursor_for_ids.execute(query, (artist_name,))
        return cursor_for_ids

    except Exception as e:
        print(e)
        exit()


def get_song_by_genre():
    '''
    Get a cursor that contains the top 300 songs that have artists that have made music in that genre sorted by popularity and song ID
    Returns:
        cursor: the cursor object with song and genre attributes to iterate over
    '''
    genre_name = flask.request.args.get('search')
    genre_name = '%' +  genre_name + '%'
    query = "\
        With SubQ1 as (SELECT artist_details.artist_id, genre_details.genre_id,genre_details.genre_name, genre_characteristics.tempo,genre_characteristics.duration,\
    genre_characteristics.danceability\
	FROM artist_details, genre_details, genre_characteristics, artist_genre_link\
	WHERE  LOWER(genre_details.genre_name) LIKE LOWER(%s)\
	AND genre_details.genre_id = genre_characteristics.genre_id\
	AND artist_details.artist_id= artist_genre_link.artist_id\
	AND genre_details.genre_id = artist_genre_link.genre_id\
	ORDER BY artist_details.artist_id)\
SELECT  song_details.song_name,SubQ1.genre_name,STRING_AGG(artist_details.artist_name, ' and ') artist_name, song_details.release_year, song_details.popularity,\
        song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability,SubQ1.tempo,SubQ1.duration,SubQ1.danceability,song_details.song_id\
        FROM song_details,song_characteristics,artist_details,song_artist_link,SubQ1\
        WHERE artist_details.artist_id= SubQ1.artist_id\
        AND song_details.song_id = song_characteristics.song_id\
        AND artist_details.artist_id = song_artist_link.artist_id\
        AND song_details.song_id = song_artist_link.song_id\
	GROUP BY song_details.song_id,song_details.song_name,song_details.release_year, song_details.popularity,\
        song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability,SubQ1.tempo,SubQ1.duration,SubQ1.danceability,SubQ1.genre_name\
        ORDER BY song_details.popularity DESC ,song_details.song_id ASC\
        LIMIT 300;"

    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (genre_name,))
        return cursor
    except Exception as e:
        print(e)
        exit()


    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (genre_name,))
        return cursor
    except Exception as e:
        print(e)
        exit()

def get_song_in_playlist(playlist_name):
    '''
    Get a cursor that contains all the songs from a specific playlist sorted by popularity and ID
    Returns:
        cursor: the cursor object to iterate over
    '''
    query="\
        With SubQ1 as (SELECT song_id FROM all_playlists WHERE playlist_name = %s ORDER BY song_id DESC OFFSET 1)\
        SELECT song_details.song_name,STRING_AGG(artist_details.artist_name, ' and ') artist_name,song_details.release_year, song_details.popularity,\
        song_characteristics.tempo, song_characteristics.duration,song_characteristics.danceability, song_details.song_id\
        FROM song_details,artist_details,SubQ1,song_artist_link,song_characteristics\
        WHERE SubQ1.song_id = song_details.song_id AND artist_details.artist_id=song_artist_link.artist_id and song_details.song_id=song_artist_link.song_id AND song_details.song_id=song_characteristics.song_id\
        GROUP BY song_details.song_name,song_details.release_year, song_details.popularity,song_characteristics.tempo,song_characteristics.duration,song_characteristics.danceability, song_details.song_id\
	    ORDER BY song_details.popularity DESC , song_details.song_id DESC;"

    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query,(playlist_name,))
        return cursor
    except Exception as e:
        print(e)
        exit()

# UNDER CONSTRUCTION: Method to get information from 2 playlists to compare them against each other
# def get_playlist_info_for_2_graph(playlist_1,playlist_2,metric):
#     '''
#     Get a cursor that contains all the song sort by year
#     Returns:
#         cursor: the cursor object to iterate over
#     '''
#     playlist_1= '%' + playlist_1 +'%'
#     playlist_2= '%' + playlist_2 +'%'
#     metric= 'song_characteristics.' + metric
#     query="\
#         With SubQ1 as (SELECT song_id,playlist_name FROM all_playlists WHERE playlist_name = %s OR playlist_name = %s ORDER BY song_id DESC OFFSET 2)\
#         SELECT SubQ1.playlist_name,song_details.song_name, song_details.song_id, %s\
#         FROM song_details,SubQ1,song_characteristics\
#         WHERE SubQ1.song_id = song_details.song_id AND song_details.song_id=song_characteristics.song_id\
# 	    ORDER BY song_details.song_name DESC , song_details.song_id DESC;"
#
#     connection = connection_to_database()
#     try:
#         cursor = connection.cursor()
#         cursor.execute(query,(playlist_1,playlist_2,metric))
#         return cursor
#     except Exception as e:
#         print(e)
#         exit()

def get_playlist_info_for_1_graph(playlist_1):
    '''
    Get a cursor that contains certain song attributes that are used for the data visualizer
    Returns:
        cursor: the cursor object to iterate over
    '''
    query="\
        With SubQ1 as (SELECT song_id,playlist_name FROM all_playlists WHERE playlist_name = %s ORDER BY song_id DESC OFFSET 1)\
        SELECT song_details.song_name, song_details.song_id, song_details.popularity,song_characteristics.tempo,song_characteristics.danceability,song_characteristics.duration\
        FROM song_details,SubQ1,song_characteristics\
        WHERE SubQ1.song_id = song_details.song_id AND song_details.song_id=song_characteristics.song_id\
	    ORDER BY song_details.song_name DESC , song_details.song_id DESC;"

    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query,(playlist_1,))
        print(cursor)
        return cursor
    except Exception as e:
        print(e)
        exit()

@api.route('/help')
def get_help():
    """return api-design.txt which describes all the requests and responses with their
    corresponding api end-points.
    """
    help_file = open('doc/api-design.txt')
    text = help_file.read()
    return flask.render_template('help.html', help_text=text)

@api.route('/search_songs')
def song_results():
    """gets a json list of dictionaries of song attributes.
    If there are more than one artists assigned to the same song with
    the same song_id, the artists will be concatonated.
    """
    cursor=get_song_by_search()
    song_details_list = []
    for row in cursor:
        song_dict = {}
        song_dict['song_name'] = row[0]
        song_dict['artist_name']= row[1]
        song_dict['release_year'] = row[2]
        song_dict['popularity'] = row[3]
        song_dict['tempo'] = row[4]
        song_dict['duration'] = row[5]
        song_dict['danceability'] = row[6]
        song_dict['song_id'] = row[7]
        song_details_list.append(song_dict)

    cursor.close()
    return json.dumps(song_details_list)

@api.route('/search_artist')
def artist_results():
    """gets a json list of dictionaries of song names and other attributes of songs
    and its artists. If there are more than one authors assigned to the same song with
    the same song_id, the artists will be concatonated.
    """
    cursor=get_song_id_by_artist()
    artist_details_list=[]
    for row in cursor:
        artist_dict={}
        artist_dict['song_name'] = row[0]
        artist_dict['artist_name'] = row[1]
        artist_dict['release_year'] = row[2]
        artist_dict['popularity'] = row[3]
        artist_dict['tempo'] = row[4]
        artist_dict['duration'] = row[5]
        artist_dict['danceability'] = row[6]
        artist_dict['artist_tempo'] = row[8]
        artist_dict['artist_duration'] = row[9]
        artist_dict['artist_danceability'] = row[10]
        artist_dict['song_id']=row[7]

        artist_details_list.append(artist_dict)

    cursor.close()
    return json.dumps(artist_details_list)



@api.route('/search_genre')
def genre_results():
    """gets a json list of dictionaries of song and genre attributes.
    If there are more than one artists assigned to the same song with
    the same song_id, the artists will be concatonated. Same songs
    may appear multiple times due to being in multiple genres
    """
    cursor=get_song_by_genre()
    genre_details_list = []
    for row in cursor:
        genre_dict = {}
        genre_dict['song_name'] = row[0]
        genre_dict['genre_name'] = row[1]
        genre_dict['artist_name'] = row[2]
        genre_dict['release_year'] = row[3]
        genre_dict['popularity'] = row[4]
        genre_dict['tempo'] = row[5]
        genre_dict['duration'] = row[6]
        genre_dict['danceability'] = row[7]
        genre_dict['genre_tempo'] = row[8]
        genre_dict['genre_duration'] = row[9]
        genre_dict['genre_danceability'] = row[10]
        genre_dict['song_id']= row[11]

        genre_details_list.append(genre_dict)

    cursor.close()
    return json.dumps(genre_details_list)


@api.route('/create_playlist')
def create():
    """sends query to create a playlist of a specific name.
    Returns a string if successful"""
    data= flask.request.get_json()
    playlist_name= data.get("new_playlist_name")
    query = "INSERT INTO all_playlists (playlist_name) VALUES (%s);"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (playlist_name,))
        connection.commit()
        cursor.close()
        return 'True'
    except Exception as e:
        print(e)
        exit()

@api.route('/delete_playlist')
def delete_playlist():
    """sends query to delete a playlist.
    Returns a string if successful"""
    data= flask.request.get_json()
    playlist_name= data.get("playlist_name")
    query = "DELETE FROM all_playlists WHERE playlist_name= %s ;"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        a=cursor.execute(query, (playlist_name,))
        connection.commit()
        cursor.close()
        return 'True'
    except Exception as e:
        print(e)
        exit()

@api.route('/insert_into_playlist')
def insert():
    """sends query to insert song_id and its corresponding playlist into
    all_playlists table dynamically.returns a string if successful"""
    data= flask.request.get_json()
    id= data.get("song_id")
    playlist_name= data.get("playlist_name")
    query = "INSERT INTO all_playlists (playlist_name,song_id) VALUES (%s,%s);"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (playlist_name,id))
        connection.commit()
        cursor.close()
        return 'True'
    except Exception as e:
        print(e)
        exit()



@api.route('/delete_from_playlist')
def delete():
    """sends query to delete song_id and its corresponding playlist from
    all_playlists table dynamically.returns a string if successful"""
    data= flask.request.get_json()
    id= data.get("song_id")
    playlist_name= data.get("playlist_name")
    query = "DELETE FROM all_playlists WHERE playlist_name = %s AND song_id=%s ;"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (playlist_name,id))
        connection.commit()
        cursor.close()
        return 'True'
    except Exception as e:
        print(e)
        exit()


@api.route('/get_song_ids_by_playlist')
def retrieve():
    """sends query to retrieve all the song_ids and their playlist names
    returns json list of dictionaries"""
    query = "SELECT * FROM all_playlists;"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        songs_playlist_list_of_dict=[]

        for row in cursor:
            song_playlist_dict = {}
            song_playlist_dict['playlist_name'] = row[0];
            song_playlist_dict['song_id'] = row[1];
            songs_playlist_list_of_dict.append(song_playlist_dict);

        cursor.close()
    except Exception as e:
        print(e)
        exit()

    return json.dumps(songs_playlist_list_of_dict)


@api.route('/playlist_menu')
def playlist_name_retriever():
    """sends query to retrieve all the playlist names and total number of songs in each playlist
    returns json list of dictionaries"""
    query = "SELECT playlist_name, COUNT(*) FROM all_playlists GROUP BY playlist_name;"
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        songs_list=[]
        for row in cursor:
            songs_dict={}
            songs_dict['playlist_name']=row[0]
            songs_dict['total_songs']=row[1]-1
            songs_list.append(songs_dict)
        cursor.close()
    except Exception as e:
        print(e)
        exit()

    return json.dumps(songs_list)

@api.route('/specific_playlist_info')
def get_specific_playlist_info():
    """sends query to retrieve details for specific playlist
    returns json list of dictionaries"""
    playlist_name = flask.request.args.get('playlist')
    cursor=get_song_in_playlist(playlist_name)
    song_details_list_playlist = []
    for row in cursor:
        song_dict = {}
        song_dict['song_name'] = row[0]
        song_dict['artist_name']= row[1]
        song_dict['release_year'] = row[2]
        song_dict['popularity'] = row[3]
        song_dict['tempo'] = row[4]
        song_dict['duration'] = row[5]
        song_dict['danceability'] = row[6]
        song_dict['song_id'] = row[7]
        song_details_list_playlist.append(song_dict)

    cursor.close()
    return json.dumps(song_details_list_playlist)

# UNDER CONSTRUCTION: endpoint to get information from 2 playlists and specific metric to be compared
# @api.route('/compare_playlists')
# def two_playlists_info():
#     """sends query to retrieve details for 2 specific playlists
#     returns json list"""
#     playlist_1 = flask.request.args.get('playlist1')
#     playlist_2 = flask.request.args.get('playlist2')
#     metric = flask.request.args.get('metric')
#     cursor=get_playlist_info_for_2_graph(playlist_1,playlist_2,metric)
#     playlist_comparator_list = []
#     for row in cursor:
#         song_dict = {}
#         song_dict['playlist_name'] = row[0]
#         song_dict['song_name']= row[1]
#         song_dict['song_id'] = row[2]
#         song_dict[metric] = row[3]
#         playlist_comparator_list.append(song_dict)
#
#     cursor.close()
#     return json.dumps(playlist_comparator_list)

@api.route('/graph_one_playlist')
def one_playlists_info():
    """sends query to retrieve a fixed set of details for 1 specific playlist
    returns json list of dictionaries"""
    playlist_1 = flask.request.args.get('playlist1')
    metric = flask.request.args.get('metric')
    cursor=get_playlist_info_for_1_graph(playlist_1)
    single_playlist_list = []
    if metric=='popularity':
        for row in cursor:
            song_dict = {}
            song_dict['song_name']= row[0]
            song_dict['song_id'] = row[1]
            song_dict['popularity'] = row[2]
            single_playlist_list.append(song_dict)

    elif metric=='tempo':
        for row in cursor:
            song_dict = {}
            song_dict['song_name']= row[0]
            song_dict['song_id'] = row[1]
            song_dict['tempo'] = row[3]
            single_playlist_list.append(song_dict)

    elif metric=='danceability':
        for row in cursor:
            song_dict = {}
            song_dict['song_name']= row[0]
            song_dict['song_id'] = row[1]
            song_dict['danceability'] = row[4]
            single_playlist_list.append(song_dict)

    elif metric=='duration':
        for row in cursor:
            song_dict = {}
            song_dict['song_name']= row[0]
            song_dict['song_id'] = row[1]
            song_dict['duration'] = row[5]
            single_playlist_list.append(song_dict)


    cursor.close()
    return json.dumps(single_playlist_list)
