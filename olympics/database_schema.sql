DROP TABLE IF EXISTS athletes;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS games_cities;
DROP TABLE IF EXISTS ages;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS medals;
DROP TABLE IF EXISTS nocs;
DROP TABLE IF EXISTS athletes_nocs;


CREATE TABLE athletes (
    id SERIAL,
    full_name text,
    sex text,
    height integer,
    weights integer
);

CREATE TABLE games (
    id SERIAL,
    games text,
    game_year integer,
    season text
);

CREATE TABLE cities (
    id SERIAL,
    city_name text
);

CREATE TABLE games_cities (
    game_id integer,
    city_id integer
);

CREATE TABLE ages (
    id SERIAL,
    athlete_id integer,
    game_id integer,
    age integer
);

CREATE TABLE events (
    id SERIAL,
    event_name text,
    sport text
);

CREATE TABLE medals (
    id SERIAL,
    athlete_id integer,
    game_id integer,
    event_id integer,
    medal text
);

CREATE TABLE nocs (
    id SERIAL,
    noc_name text,
    region text,
    notes text
);

CREATE TABLE athletes_nocs (
    athlete_id integer,
    noc_id integer
);