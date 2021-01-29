CREATE TABLE athlete_info(
    athlete_id text,
    athlete_name text,
    team_id text);

CREATE TABLE noc_info(
    noc_id text, 
    noc text, 
    region text);
    
CREATE TABLE team_info(
    team_id text, 
    team text, 
    noc_id text);
    
CREATE TABLE events_info(
    games_id text,
    games text,
    year_name text,
    event_name text,
    athlete_id text,
    medal text,
    noc_id text);
