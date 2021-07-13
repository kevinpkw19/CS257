"""authors: Kevin Phung, Kyosuke Imai"""
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
# @app.route("/<string:path>")
@app.route('/<path:path>', methods=['GET', 'POST'])
def shared_header_catchall(path):

    if path== 'api/playlist_menu_page':
        return flask.render_template('allPlaylists.html')

    elif path == 'api/insert_into_playlist':
        return api.insert()

    elif path == 'api/delete_from_playlist':
        return api.delete()

    elif path == 'api/create_playlist':
        api.create()
        return flask.render_template('allPlaylists.html')

    elif path == 'api/delete_playlist':
        api.delete_playlist()
        return flask.render_template('allPlaylists.html')

    elif path == 'api/specific_playlist_page':
        return flask.render_template('yourPlaylist.html')

    elif path == 'api/data_visualizer':
        return flask.render_template('dataVisualizer.html')

    else:
        return flask.render_template('index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tiny Flask application, including API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
