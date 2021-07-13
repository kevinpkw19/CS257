import csv
import ast


#main class for songs
class song_row:
    def __init__(self, song_name, artist, release_year, popularity, tempo, duration,danceability):
        self.song_name = song_name
        self.artist= artist
        self.release_year = release_year
        self.popularity = popularity
        self.tempo = tempo
        self.duration = duration
        self.danceability = danceability

# class which stores all song details
class song_details:
    def __init__(self, name, artists_name, release_year,popularity):
        self.name = name
        self.artists_name = artists_name
        self.release_year = release_year
        self.popularity= popularity

#creates the song details table we use in the database
def create_song_details_table(all_rows):
    song_details_table = []
    song_details_dict = {}
    index = 1
    for song_row in all_rows:
        one_song_details = song_details(song_row.song_name, song_row.artist, song_row.release_year, song_row.popularity)
        if one_song_details not in song_details_dict:
            this_row = [index, song_row.song_name, song_row.artist, song_row.release_year, song_row.popularity]
            song_details_table.append(this_row)
            song_details_dict[one_song_details] = index
            index = index + 1
    return song_details_table, song_details_dict


# class which stores all song characteristics
class song_characteristics:
	def __init__(self, tempo, duration, danceability):
		self.tempo = tempo
		self.duration = duration
		self.danceability = danceability

#creates the song characteristics table we use in the database
def create_song_characteristics_table(all_rows):
    song_characteristics_table = []
    song_characteristics_dict = {}
    index = 1
    for song_row in all_rows:
        one_song_characteristics = song_characteristics(song_row.tempo, song_row.duration, song_row.danceability)
        if one_song_characteristics not in song_characteristics_dict:
            this_row = [index, song_row.tempo, song_row.duration, song_row.danceability]
            song_characteristics_table.append(this_row)
            song_characteristics_dict[one_song_characteristics] = index
            index = index + 1
    return song_characteristics_table, song_characteristics_dict

#main artist class
class artist_row:
    def __init__(self, artist_name, tempo, duration,danceability,genres):
        self.artist_name = artist_name
        self.tempo = tempo
        self.duration = duration
        self.danceability = danceability
        self.genres= genres

#class which stores artist details
class artist_details:
    def __init__(self, name,genres):
        self.name = name
        self.genres= genres

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other

# creates the artist details table we use in the database
def create_artist_details_table(all_rows):
    artist_details_table = []
    artist_details_dict = {}
    index = 1
    for artist_row in all_rows:
        one_artist_details = artist_details(artist_row.artist_name, artist_row.genres)
        if one_artist_details not in artist_details_dict:
            this_row = [index, artist_row.artist_name]
            artist_details_table.append(this_row)
            artist_details_dict[one_artist_details] = index
            index = index + 1
    return artist_details_table, artist_details_dict

# Class which stores all artist characteristics
class artist_characteristics:
	def __init__(self, tempo, duration, danceability):
		self.tempo = tempo
		self.duration = duration
		self.danceability = danceability

#creates the artist characteristics table we use in the database
def create_artist_characteristics_table(all_rows):
    artist_characteristics_table = []
    artist_characteristics_dict = {}
    index = 1
    for artist_row in all_rows:
        one_artist_characteristics = artist_characteristics(artist_row.tempo, artist_row.duration, artist_row.danceability)
        if one_artist_characteristics not in artist_characteristics_dict:
            this_row = [index, artist_row.tempo, artist_row.duration, artist_row.danceability]
            artist_characteristics_table.append(this_row)
            artist_characteristics_dict[one_artist_characteristics] = index
            index = index + 1
    return artist_characteristics_table, artist_characteristics_dict

#creates the song artist linking table we use in the database
def create_song_artist_link_table(song_details_dict,artist_details_dict):
    link_table=[]
    for item in song_details_dict:
        song_ID= song_details_dict.get(item)
        str_artists_names=item.artists_name
        artist_list=ast.literal_eval(str_artists_names)
        for artist in artist_list:
            if artist!='n/a':
                artist_ID= artist_details_dict.get(artist)
                this_row=[song_ID,artist_ID]
                link_table.append(this_row)

    return link_table

#---------------------------------------------------------------------
#main genre class
class genre_row:
    def __init__(self, genre_name, tempo, duration,danceability):
        self.genre_name = genre_name
        self.tempo = tempo
        self.duration = duration
        self.danceability = danceability

#class to store genre details
class genre_details:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other

#Creates the genre details table we use in the database
def create_genre_details_table(all_rows):
    genre_details_table = []
    genre_details_dict = {}
    index = 1
    for genre_row in all_rows:
        one_genre_details = genre_details(genre_row.genre_name)
        if one_genre_details not in genre_details_dict:
            this_row = [index, genre_row.genre_name,]
            genre_details_table.append(this_row)
            genre_details_dict[one_genre_details] = index
            index = index + 1
    return genre_details_table, genre_details_dict

#class to store genre characteristics
class genre_characteristics:
	def __init__(self, tempo, duration, danceability):
		self.tempo = tempo
		self.duration = duration
		self.danceability = danceability

#Creates the genre characteristics table we use in the database
def create_genre_characteristics_table(all_rows):
    genre_characteristics_table = []
    genre_characteristics_dict = {}
    index = 1
    for genre_row in all_rows:
        one_genre_characteristics = genre_characteristics(genre_row.tempo, genre_row.duration, genre_row.danceability)
        if one_genre_characteristics not in genre_characteristics_dict:
            this_row = [index, genre_row.tempo, genre_row.duration, genre_row.danceability]
            genre_characteristics_table.append(this_row)
            genre_characteristics_dict[one_genre_characteristics] = index
            index = index + 1
    return genre_characteristics_table, genre_characteristics_dict

#Creates the artist genre linking table we use in the database
def create_artist_genre_link_table(artist_details_dict,genre_details_dict):
    link_table=[]
    for item in artist_details_dict:
        artist_ID= artist_details_dict.get(item)
        str_genres_names=item.genres
        genres_list=ast.literal_eval(str_genres_names)
        for genres in genres_list:
            genre_ID= genre_details_dict.get(genres)
            this_row=[artist_ID,genre_ID]
            link_table.append(this_row)

    return link_table



#---------------------------------------------------------
#Makes the CSV rows that we'll be using
def make_csv_row(this_row):
	if len(this_row) < 1:
		print("yooo! your row aint right!")
		return
	out_csv_row = str(this_row[0])
	for i in range(1, len(this_row)):
		csv_save_cell = str(this_row[i]).replace(",", " ").replace('"', "(", 1)
		csv_save_cell = csv_save_cell.replace('"', ")")
		out_csv_row = out_csv_row + "," + csv_save_cell

	return (out_csv_row + '\n')

def print_table(table_list, file_name, header_list):
	"""print method to print the tables into a csv file given the table list, file name and the header of the individual columns """
	num_col = len(table_list[0])
	if num_col != len(header_list):
		print("error. the number of cols between your list and header_list doesn't match!")
		print(num_col)
		print(len(header_list))
		return

	outfile = open(file_name, 'w')
	outfile.write(make_csv_row(header_list))

	# write actual data
	for row in table_list:
		outfile.write(make_csv_row(row))
	outfile.close()

# main function that makes all the csv files used to upload into the database
def main():
    #----------------------------------------------------------------------------
    song_rows = []
    for song_roww in song_rows:
        print(song_roww)
    with open('data.csv') as file:
        read_in_file = list((csv.reader(file, skipinitialspace=True)))

    for row in read_in_file[1:]:
        if len(row) > 1:
            tempo=float(row[16])
            danceability=float(row[2])
            tempo=round(tempo,2)
            danceability=round(danceability,2)
            this_row = song_row(row[12], row[1], row[18], row[13], tempo, row[3], danceability)
            song_rows.append(this_row)


    song_details_table, song_details_dict = create_song_details_table(song_rows)
    song_details_header =["song_ID", "song_name", "artist_names", "release_year","popularity"]
    print_table(song_details_table, "song_details.csv", song_details_header)

    song_characteristics_table, song_characteristics_dict = create_song_characteristics_table(song_rows)
    song_characteristics_header = ["song_ID", "tempo", "duration","danceability"]
    print_table(song_characteristics_table, "song_characteristics.csv", song_characteristics_header)

    #--------------------------------------------------------------------------------------
    artist_rows = []
    with open('data_w_genres.csv') as file:
        read_in_file = list((csv.reader(file, skipinitialspace=True)))

    for row in read_in_file[1:]:
        if len(row) > 1:
            tempo= float(row[9])
            danceability=float(row[2])
            duration= float(row[3])
            tempo= round(tempo,2)
            danceability=round(danceability,2)
            duration= round(duration,1)
            this_row = artist_row(row[0], tempo, duration, danceability,row[15])
            artist_rows.append(this_row)

    artist_details_table, artist_details_dict = create_artist_details_table(artist_rows)
    artist_details_header =["artist_ID", "artist_name"]
    print_table(artist_details_table, "artist_details.csv", artist_details_header)

    artist_characteristics_table, artist_characteristics_dict = create_artist_characteristics_table(artist_rows)
    artist_characteristics_header = ["artist_ID", "average tempo", " average duration","average danceability"]
    print_table(artist_characteristics_table, "artist_characteristics.csv", artist_characteristics_header)

    #---------------------------------------------------------------------------------
    genre_rows = []
    with open('data_by_genres.csv') as file:
        read_in_file = list((csv.reader(file, skipinitialspace=True)))

    for row in read_in_file[1:]:
        if len(row) > 1:
            tempo=float(row[9])
            danceability=float(row[2])
            duration= float(row[3])
            tempo=round(tempo,2)
            danceability=round(danceability,2)
            duration=round(duration,1)
            this_row = genre_row(row[0], tempo, duration, danceability)
            genre_rows.append(this_row)


    genre_details_table, genre_details_dict = create_genre_details_table(genre_rows)
    genre_details_header =["genre_ID", "genre_name"]
    print_table(genre_details_table, "genre_details.csv", genre_details_header)

    genre_characteristics_table, genre_characteristics_dict = create_genre_characteristics_table(genre_rows)
    genre_characteristics_header = ["genre_ID", "average tempo", " average duration","average danceability"]
    print_table(genre_characteristics_table, "genre_characteristics.csv", genre_characteristics_header)

    #---------------------------------------------------------------
    song_artist_linking_table = create_song_artist_link_table(song_details_dict,artist_details_dict)
    song_artist_linking_table_header =["song_ID","artist_ID"]
    print_table(song_artist_linking_table, "song_artist_link.csv", song_artist_linking_table_header)

    artist_genre_linking_table = create_artist_genre_link_table(artist_details_dict,genre_details_dict)
    artist_genre_linking_table_header =["artist_ID", "genre_ID"]
    print_table(artist_genre_linking_table, "artist_genre_link.csv", artist_genre_linking_table_header)


if __name__ == '__main__':
    main()
