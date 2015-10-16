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

CREATE VIEW v_performance_table as 
		select name, table1.player_id, no_of_wins, total_games
		from (select players.name, players.player_id, count(win_ref) as no_of_wins
            from players left join games on players.player_id = games.win_ref 
            group by players.player_id) as table1
            join (select players.player_id, count(*) as total_games from players left join games 
            on players.player_id = games.win_ref OR players.player_id = games.loose_ref
            group by players.player_id) as table2 on table1.player_id = table2.player_id 
            order by no_of_wins desc;

CREATE VIEW v_lost_games as
            select players.player_id, count(loose_ref) as lost_games from 
            players left join games on players.player_id = games.loose_ref 
            group by players.player_id;

CREATE VIEW v_won_games as
            select players.name, players.player_id, count(win_ref) as wins 
            from players left join games on players.player_id = games.win_ref 
            group by players.player_id;

CREATE VIEW v_combined_standings as
            select name, table1.player_id, wins, lost_games
            from (select players.name, players.player_id, count(win_ref) as wins
            from players left join games on players.player_id = games.win_ref
            group by players.player_id) as table1
            join (select players.player_id, count(loose_ref) as lost_games from 
            players left join games on players.player_id = games.loose_ref 
            group by players.player_id) as table2 on table1.player_id = table2.player_id 
            order by wins desc;

CREATE VIEW player_standings as
            select v_won_games.player_id, name, v_won_games.wins, total_games from 
            v_won_games join (select player_id, SUM(wins + lost_games) as total_games 
            from v_combined_standings group by player_id) as totaltable 
            on v_won_games.player_id = totaltable.player_id order by wins desc;


