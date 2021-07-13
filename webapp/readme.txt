AUTHORS: Kevin Phung, Kyosuke Imai

*IMPORTANT*: Will need to import simplejson module for the program to work

DATA:
  Description: The dataset file contains more than 175000 songs collected from the Spotify Web API, each with individual metrics like tempo, danceability and popularity.
  Link to dataset: https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks
  Copyright Info.: Community Data License Agreement – Sharing – Version 1.0

STATUS:
  -Features Working:
    >Search by Categories (Song,Artist,genre): Users can search for songs using one of the 3 Categories

    >Sort search results: Users can sort all results by any one of the metrics(song_name, release_year, danceability, etc.)

    >Create/Delete Playlists: Users can create and delete playlists dynamically

    >Add/Delete from Playlist: Users can add and delete songs from playlist(no duplicates allowed)

    >Download Playlist Content as CSV file ("Playlist_Name.csv")

    >Users can compare song metrics within one playlist using a visualizer.


  -Features Not Implemented:
    >long in/sign up function

    >compare two playlists in data visualizer
