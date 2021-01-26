


CREATE TABLE athlete (
    id SERIAL,
    full_name text,
    sex text,
    height integer,
    weight integer
);

CREATE TABLE games (
    id SERIAL,
    games text,
    game_year integer,
    season text

);

CREATE TABLE city (
    id SERIAL,
    city_name text
);

CREATE TABLE game_city (
    id SERIAL,
    games_id integer,
    city_id integer
);




\copy athlete from 'athlete_events.csv' DELIMITER ',' CSV NULL AS 'NULL'