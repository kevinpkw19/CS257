SELECT NOC FROM noc_info
ORDER BY NOC;

SELECT athlete_info.athlete_name, athlete_info.team_id, team_info.team_id, team_info.team 
FROM athlete_info, team_info
WHERE athlete_info.team_id = team_info.team_id 
AND team_info.team = 'Kenya'
ORDER BY athlete_name;

SELECT athlete_info.athlete_name, athlete_info.athlete_id, events_info.medal, events_info.year_name, events_info.athlete_id
FROM athlete_info, events_info
WHERE athlete_info.athlete_name = 'Gregory Efthimios "Greg" Louganis' 
AND athlete_info.athlete_id = events_info.athlete_id
AND events_info.medal != 'NA'
ORDER BY year_name;

SELECT events_info.athlete_id, COUNT(events_info.medal), athlete_info.athlete_id, athlete_info.team_id, team_info.team_id, team_info.noc_id, noc_info.id, noc_info.noc
FROM events_info, athlete_info, team_info, noc_info
WHERE events_info.medal = 'Gold'
AND events_info.athlete_id = athlete_info.athlete_id
AND athlete_info.team_id = team_info.team_id
AND team_info.noc_id = noc_info.id
ORDER BY noc_info.noc;


SELECT events_info.athlete_id, COUNT(events_info.medal), athlete_info.athlete_id, athlete_info.team_id, team_info.team_id, team_info.noc_id, noc_info.id, noc_info.noc
FROM events_info, athlete_info, team_info, noc_info
WHERE events_info.medal = 'Gold'
AND events_info.athlete_id = athlete_info.athlete_id
AND athlete_info.team_id = team_info.team_id
AND team_info.noc_id = noc_info.id
GROUP BY events_info.athlete_id, events_info.medal, athlete_info.athlete_id, athlete_info.team_id, team_info.team_id, team_info.noc_id, noc_info.id, noc_info.noc
ORDER BY events_info.medal;
-- ORDER BY COUNT(events_info.medal);



