#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate the games table only, preserving player records.
    c.execute("TRUNCATE TABLE games;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate both the players and games tables from the database.
    c.execute("TRUNCATE TABLE players, games")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(player_id) FROM players;")
    count_result = c.fetchone()
    return count_result[0]
    conn.commit()
    conn.close()


def registerPlayer(name, tourn_id=1):
    """Registers a player into the players table, along with a unique player id """

    conn = connect()
    c = conn.cursor()
    if tourn_id==2:
        query = "INSERT INTO players_2 (name) VALUES (%s);"
    else:
        query = "INSERT INTO players (name) VALUES (%s);"
    c.execute(query, (name,))
    conn.commit()
    conn.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    # Use the view player_standings as defined within tournament.sql
    c.execute("SELECT * FROM player_standings;")
    performance_table = c.fetchall()
    return performance_table
    conn.commit()
    conn.close()



def reportMatch(winner, loser):

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    # Query and execute code format to escape the string, avoiding SQL injection.
    query = "INSERT INTO games (win_ref, loose_ref) VALUES (%s, %s);"
    c.execute(query, (winner, loser))
    conn.commit()
    conn.close()

 
 
def swissPairings():

    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    # Use the view v_swiss_pairings as defined within tournament.sql
    c.execute("SELECT * FROM v_swiss_pairings;")
    result = c.fetchall()
    return result
    conn.commit()
    conn.close()

    """
    # Obtain the player standings tuples from the playerStandings() function.
    player_standings = playerStandings()

    # Define an empty dataset ready for tuple insertion below.
    pairing_results = []

    # Iterate through the names and id's of players, and create associated pairing tuples.
    for i in range(0, (len(player_standings)-1), 2):
        one, two = player_standings[i][0], player_standings[i+1][1]
        three, four = player_standings[i+1][0], player_standings[i+1][1]
        pairing_results.append((one, two, three, four))
    
    return pairing_results
    """
