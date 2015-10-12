-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (player_id serial PRIMARY KEY,
					  name varchar(40));

CREATE TABLE games (id serial PRIMARY KEY,
					win_ref integer REFERENCES players (player_id),
					loose_ref integer REFERENCES players (player_id));

