SELECT NOC FROM noc_info
ORDER BY NOC;

SELECT athlete_info.athlete_name, team_info.team 
FROM athlete_info, team_info
WHERE athlete_info.team_id = team_info.team_id 
AND team_info.team = 'Kenya'
ORDER BY athlete_name;

SELECT athlete_info.athlete_name, events_info.medal, events_info.games, events_info.event_name
FROM athlete_info, events_info
WHERE athlete_info.athlete_name = 'Gregory Efthimios "Greg" Louganis' 
AND athlete_info.athlete_id = events_info.athlete_id
AND events_info.medal != 'NA'
ORDER BY year_name;

SELECT COUNT(events_info.medal), noc_info.noc 
FROM events_info
INNER JOIN noc_info ON events_info.noc_id = noc_info.id
WHERE events_info.medal = 'Gold'
AND events_info.noc_id = noc_info.id
GROUP BY events_info.medal, noc_info.noc 
ORDER BY COUNT(events_info.medal) DESC;



