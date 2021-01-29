# Made by Aishwarya Varma and Kevin Phung
# Date: 1/29/2021

import argparse
import psycopg2

from config import database
from config import user
from config import password


def connect_to_database(query,search_string= None):
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    try:
        cursor = connection.cursor()
        if search_string != None:
            cursor.execute(query, (search_string,))
        else:
            cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    display_results(cursor)
    connection.close()


def display_results(cursor):
    print('\n')
    for row in cursor:
        for column in row:
            print(column, end = " ---------- ")
        print()
    print()


def create_athletes_by_noc_query(noc_input):
    search_string= "'{}'".format(str(noc_input))
    query ="SELECT athlete_info.athlete_name FROM athlete_info, team_info, noc_info WHERE noc_info.noc = " + search_string + " AND athlete_info.team_id = team_info.team_id AND team_info.noc_id = noc_info.noc_id ORDER BY athlete_info.athlete_name;"
    # "SELECT athlete_info.athlete_name FROM athlete_info, team_info, noc_info WHERE noc_info.noc = '{}' AND athlete_info.team_id = team_info.team_id AND team_info.noc_id = noc_info.noc_id ORDER BY athlete_info.athlete_name;".format(noc_input)
    print('===== All athletes from {} ====='.format(noc_input))
    connect_to_database(query,search_string)

def create_gold_medals_by_noc_query():
    query = "SELECT COUNT(events_info.medal), noc_info.noc FROM events_info INNER JOIN noc_info ON events_info.noc_id = noc_info.noc_id WHERE events_info.medal = 'Gold' AND events_info.noc_id = noc_info.noc_id GROUP BY events_info.medal, noc_info.noc ORDER BY COUNT(events_info.medal) DESC;"
    print('===== Gold Medals per NOC in decreasing order =====')
    connect_to_database(query)


def create_athlete_by_gold_medals_query(athlete_input):
    search_string = "'%{}%'".format(str(athlete_input))
    query = "SELECT athlete_info.athlete_name, COUNT(events_info.medal) FROM athlete_info, events_info WHERE events_info.medal = 'Gold' AND athlete_info.athlete_name LIKE "+ search_string + " AND athlete_info.athlete_id = events_info.athlete_id GROUP BY athlete_info.athlete_name;"
    print(('===== Gold Medals that match search string "{}" =====').format(athlete_input))
    connect_to_database(query)


def get_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--athlete_by_noc", "-a", action="store_true", help = "Accepts a National Olympic Committee(NOC) as the parameter and returns a list of all the athletes from that NOC")
    group.add_argument("--noc_by_gold", "-n", action="store_true", help = "Lists all National Olympic Committees(NOC) by decreasing gold medal count")
    group.add_argument("--gold_by_athlete", "-g", action="store_true", help = "Accepts a search string as a parameter and lists the athletes that match the search string that have won gold medals and their corresponding gold medal count, if they have won any.")
    parser.add_argument("Input", nargs = "*", type=str, help = "for --athlete_by_noc, provide an NOC. for --gold_by_athlete, provide athlete name.")

    args = parser.parse_args()

    return args

def main():
    args = get_arguments()

    # If user writes command without input, print error message
    if len(args.Input) == 0:
        if args.noc_by_gold:
            create_gold_medals_by_noc_query()
        else:
            print("Your must use --noc_by_gold if you don't provide any input parameters.")

    # checks the number of inputs given by user and prints error message accordingly
    elif len(args.Input) == 1:
        if args.gold_by_athlete:
            create_athlete_by_gold_medals_query(args.Input[0])
        elif args.athlete_by_noc:
            create_athletes_by_noc_query(args.Input[0])

    else:
        print("Error. Too many arguments.")


main()
