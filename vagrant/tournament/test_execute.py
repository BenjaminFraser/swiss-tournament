import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    c.execute("select name, table1.player_id, no_of_wins, total_games " 
              "from (select players.name, players.player_id, count(win_ref) as no_of_wins " 
              "from players left join games on players.player_id = games.win_ref " 
              "group by players.player_id) as table1 " 
              "join (select players.player_id, count(*) as total_games from players join games " 
              "on players.player_id = games.win_ref OR players.player_id = games.loose_ref " 
              "group by players.player_id) as table2 on table1.player_id = table2.player_id " 
              "order by no_of_wins desc;")
    performance_results = c.fetchall()
    print len(performance_results)
    conn.commit()
    conn.close()

playerStandings()