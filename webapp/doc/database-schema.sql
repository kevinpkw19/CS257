CREATE TABLE artist_details (
  artist_id int,
  artist_name text
);

  CREATE TABLE artist_characteristics (
    artist_id int,
    tempo decimal,
    duration decimal,
    danceability decimal
  );

CREATE TABLE song_details (
  song_id int,
  song_name text,
  artists text,
  release_year int,
  popularity int
);

CREATE TABLE song_characteristics (
  song_id int,
  tempo decimal,
  duration decimal,
  danceability decimal
);


CREATE TABLE genre_details (
  genre_id int,
  genre_name text
);

CREATE TABLE genre_characteristics (
  genre_id int,
  tempo decimal,
  duration decimal,
  danceability decimal
);

CREATE TABLE song_artist_link (
  song_id int,
  artist_id int
);

CREATE TABLE artist_genre_link (
  artist_id int,
  genre_id int
);

CREATE TABLE all_playlists (
  playlist_name text,
  song_id int
);


-- CREATE TABLE temp_playlists (
--   song_id int
-- );
