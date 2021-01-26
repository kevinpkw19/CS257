SELECT NOC FROM noc_info
ORDER BY NOC;

SELECT athlete_name, team_id, team FROM athlete_info, team_info
WHERE athlete_info.team_id = team_info.team_id 
AND team_info.team = 'Kenya'
ORDER BY athlete_name;

SELECT athlete_name, athlete_id, medal,event_name, games, year_name
FROM athlete_info, events_info
WHERE athlete_info.athlete_name = 'Greg Louganis' 
AND athlete_info.athlete_id = events_info.athlete_id
AND events_info.medal != 'N/A'
ORDER BY year_name;



