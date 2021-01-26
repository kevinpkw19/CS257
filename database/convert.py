# Authors: Kevin Phung and Aishwarya Varma
# Date: 1/26/2020

import csv

noc_dictionary={}

with open('noc_regions.csv') as csvfile:
    with open('noc_info.csv', 'w', newline="") as writefile1:
        line_reader = csv.reader(csvfile, delimiter = ',')
        line_writer2 = csv.writer(writefile1, delimiter = ',')
        next(csvfile)
        for line in line_reader:
            noc = line[0]
            if noc not in noc_dictionary:
                noc_dictionary[noc] = {"id" : len(noc_dictionary) + 1, "region" : line[1]}
        for noc in noc_dictionary:
            noc_id = noc_dictionary.get(noc).get("id")
            noc_region = noc_dictionary.get(noc).get("region")
            line_writer2.writerow([noc_id, noc, noc_region])

team_dictionary={}

with open('athlete_events.csv') as csvfile:
    with open('team_info.csv', 'w', newline="") as writefile2:
        line_reader = csv.reader(csvfile, delimiter = ',')
        line_writer2 = csv.writer(writefile2, delimiter = ',')
        next(csvfile)
        for line in line_reader:
            team = line[6]
            noc = line[7]
            if team not in team_dictionary:
                if noc_dictionary.get(noc)!= None:
                    noc_id = noc_dictionary.get(noc).get("id")
                    team_dictionary[team] = {"id" : len(team_dictionary) + 1, "noc_id" : noc_id}
        for team in team_dictionary:
            team_id = team_dictionary.get(team).get("id")
            noc_id_cur = team_dictionary.get(team).get("noc_id")
            line_writer2.writerow([team_id, team, noc_id_cur])


athlete_dictionary = {}

with open('athlete_events.csv') as csvfile:
    with open('athlete_info.csv', 'w', newline = "") as writefile3:
        line_reader = csv.reader(csvfile, delimiter = ',')
        line_writer3 = csv.writer(writefile3, delimiter = ',')
        next(csvfile)
        for line in line_reader:
            name_id = line[0]
            name = line[1]
            team = line[6]
            if name not in athlete_dictionary:
                if team_dictionary.get(team)!= None:
                    team_id = team_dictionary.get(team).get("id")
                    athlete_dictionary[name] = {"id" : name_id, "team_id" : team_id}
        for athlete in athlete_dictionary:
            team_id = athlete_dictionary.get(athlete).get("team_id")
            name_id = athlete_dictionary.get(athlete).get("id")
            line_writer3.writerow([name_id, athlete, team_id])
        
games_dictionary = {}
with open('athlete_events.csv') as csvfile:
    with open('events_info.csv', 'w', newline = "") as writefile4:
        line_reader = csv.reader(csvfile, delimiter = ',')
        line_writer4 = csv.writer(writefile4, delimiter = ',')

        next(csvfile)
        for line in line_reader:
            games = line[8]
            year = line[9]
            athlete = line[1]
            event = line[13]
            medal = line[14]
            noc = line[7]
            if games not in games_dictionary:
                games_dictionary[games] = len(games_dictionary)+1
            if athlete_dictionary.get(athlete)!= None and noc_dictionary.get(noc)!= None:
                athlete_id = athlete_dictionary.get(athlete).get("id")
                games_id = games_dictionary.get(games)
                noc_id = noc_dictionary.get(noc).get("id")
                line_writer4.writerow([games_id, games, year, event, athlete_id,medal,noc_id])








                