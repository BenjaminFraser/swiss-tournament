-- Table definitions and custom views for the tournament project.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (player_id serial PRIMARY KEY,
					  name varchar(40));

CREATE TABLE games (id serial PRIMARY KEY,
					win_ref integer REFERENCES players (player_id),
					loose_ref integer REFERENCES players (player_id));

-- Create a view that lists a player_id along with associated loss record.
CREATE VIEW v_lost_games as
            select players.player_id, count(loose_ref) as lost_games from 
            players left join games on players.player_id = games.loose_ref 
            group by players.player_id;

-- Create a view that displays a players id, name and win count to aid further views.
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

-- Create a view that combines the id, name and won games from combined standings, with 
-- a new column called total_games, which is derived from wins + lost games.
CREATE VIEW player_standings as
            select v_won_games.player_id, name, v_won_games.wins, total_games from 
            v_won_games join (select player_id, SUM(wins + lost_games) as total_games 
            from v_combined_standings group by player_id) as totaltable 
            on v_won_games.player_id = totaltable.player_id order by wins desc;


-- Number each player standing row through adding a row number with row_number().
CREATE VIEW ranked_standings as 
            select row_number() over (order by wins desc) 
            as rank, player_id, name, wins, total_games from player_standings;


-- Perform a self-join on view ranked_standings to produce a swiss pairings view with
-- player 1 id and name, and player 2 id and name on the same row. 
CREATE VIEW v_swiss_pairings as 
            select a.player_id AS "player_1_id", a.name AS "player_1_name", 
            b.player_id AS "player_2_id", b.name AS "player_2_name"
            from ranked_standings a, ranked_standings b 
            WHERE a.rank+1 = b.rank AND a.rank % 2 = 1;


