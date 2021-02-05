-- Author: Aiden Chang, Sky Lu

-- SELECT nocs.noc_name 
-- FROM nocs
-- ORDER BY nocs.noc_name;

-- SELECT athletes.full_name, nocs.noc_name
-- FROM athletes, nocs, athletes_nocs
-- WHERE athletes.id = athletes_nocs.athlete_id
-- AND nocs.id = athletes_nocs.noc_id
-- AND nocs.region = 'Kenya';

-- SELECT DISTINCT athletes.full_name, nocs.noc_name, games.games
--                  FROM athletes, nocs, athletes_nocs, games, medals
--                  WHERE athletes.id = athletes_nocs.athlete_id
--                  AND nocs.id = athletes_nocs.noc_id
--                  AND athletes.id = medals.athlete_id
--                  AND games.id = medals.game_id
--                  AND lower(games.games) = '1984 summer'
--                  ORDER BY athletes.full_name;

-- SELECT athletes.full_name, nocs.noc_name, DISTINCT games.games
-- FROM
-- athletes,
-- nocs,
-- athletes_nocs,
-- medals,
-- games
-- WHERE athletes.id = athletes_nocs.athlete_id
-- AND nocs.id = athletes_nocs.noc_id
-- AND athletes.id = medals.athlete_id
-- AND games.id = medals.game_id
-- AND games.games = '2006 Winter';

-- SELECT games.games, events.event_name, medals.medal
-- FROM games, events, medals, athletes
-- WHERE athletes.id = medals.athlete_id
-- AND games.id = medals.game_id
-- AND events.id = medals.event_id
-- AND athletes.full_name LIKE '%Greg%%Louganis%'
-- ORDER BY games.game_year;

-- SELECT nocs.noc_name, COUNT(medals.medal)
-- FROM nocs, athletes, medals, athletes_nocs, games
-- WHERE athletes.id = medals.athlete_id
-- AND games.id = medals.game_id
-- AND athletes.id = athletes_nocs.athlete_id
-- AND nocs.id = athletes_nocs.noc_id
-- AND medals.medal = 'Gold'
-- AND games.game_year = '2018'
-- GROUP BY nocs.noc_name
-- ORDER BY COUNT(medals.medal) DESC;

-- SELECT DISTINCT games.game_year, games.season, cities.city_name
-- FROM games, cities, games_cities
-- WHERE games.id = games_cities.game_id
-- AND cities.id = games_cities.city_id
-- ORDER BY games.game_year;

-- SELECT DISTINCT nocs.noc_name, nocs.region
-- FROM nocs
-- ORDER BY nocs.noc_name;

SELECT DISTINCT athletes.id, athletes.full_name, athletes.sex, 
events.event_name, medals.medal
FROM athletes, events, medals, games, athletes_nocs, nocs
WHERE athletes.id = medals.athlete_id
AND events.id = medals.event_id
AND games.id = medals.game_id
AND athletes.id = athletes_nocs.athlete_id
AND nocs.id = athletes_nocs.noc_id
AND medals.medal IS NOT NULL
AND games.id = 23
AND nocs.noc_name = 'USA'
ORDER BY athletes.full_name;
