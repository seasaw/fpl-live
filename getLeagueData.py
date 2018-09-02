import requests
import json


MYLEAGUEID = "257477"
MYTEAMID = "1142621"
WEEKID = "4"

BASEURL = "https://fantasy.premierleague.com/drf/"

LEAGUEDATAURL = "https://fantasy.premierleague.com/drf/leagues-classic-standings/"

TEAMDATAURLSTART = "https://fantasy.premierleague.com/drf/entry/"
TEAMDATAURLEND = "/event/4/picks"

LIVEDATAURL = "https://fantasy.premierleague.com/drf/event/4/live"

PLAYERSDATAURL = "https://fantasy.premierleague.com/drf/bootstrap-static"


#get json function for a given url
def get_data(api_url, leagueid="", end_url=""):
    league_url = api_url + leagueid + end_url
    r = requests.get(league_url)
    return r.json()

#get list of all players in the game
def get_all_players_data():
    player_data = get_data(PLAYERSDATAURL)
    return player_data["elements"]

#get current live score data
def get_live_data():
    return get_data(LIVEDATAURL)


#get list of team data for teams in league given an id,
#returns list of dicts like:
# "id": 5829458,
# "entry_name": "Marchester United",
# "event_total": 89,
# "player_name": "joe march",
# "movement": "new",
# "own_entry": true,
# "rank": 1,
# "last_rank": 0,
# "rank_sort": 1,
# "total": 89,
# "entry": 1142621,
# "league": 257477,
# "start_event": 1,
# "stop_event": 38
def get_teams_in_league(league_id=MYLEAGUEID):
    league_data = get_data(LEAGUEDATAURL, league_id)
    return league_data["standings"]["results"]


#get points for team #return points
#still need to check if game is live
# need to add bonus if  live
def get_points_for_team(team_id, player_data, live_data):
    #get players in team
    all_players_in_team = get_players_for_team(str(team_id))
    # loop
    points = []
    for player in all_players_in_team:
        # get player data from id
        player_info = get_player_info(player["element"], player_data)
        # get points for player
        player_points = get_live_points_for_player(player_info, live_data)
        points.append(player_points["stats"]["total_points"])
    return points[0:10]


#get player data for team id
def get_player_data_for_team(team_id, player_data, live_data):
    #get players in team
    all_players_in_team = get_players_for_team(str(team_id))
    # loop
    players = []
    for player in all_players_in_team:
        # get player data from id
        player_info = get_player_info(player["element"], player_data)
        player_info["live_points"] = get_live_points_for_player(player_info, live_data)
        players.append(player_info)
    return players



#get list of players in a team for a given id #return player data
#returns
# 'element': 260,
# 'position': 1,
# 'is_captain': False,
# 'is_vice_captain': False,
# 'multiplier': 1
def get_players_for_team(team_id=MYTEAMID):
    team_data = get_data(TEAMDATAURLSTART, str(team_id), TEAMDATAURLEND)
    return team_data["picks"]



#get data for individual player given player id #return playerdata
def get_player_info(player_id, data):
    for player in data:
        if player["id"] == player_id:
            return player
    return {}


#get points for player from live data
def get_live_points_for_player(player_id, live_data):
    player_id = str(player_id["id"])
    return live_data["elements"][player_id]

def get_bp_for_player(player_id):
    return 0


#get bonus points for player #return 1, 2, 3, 0

#get bonus point players for team #return top 3 player
# s ids


def main():
    player_data = get_all_players_data()
    live_data = get_live_data()

    #get teams in league
    teams_in_league = get_teams_in_league()

    #todo: get bonus points for game playing
    """teams_dict = {}
    for team in teams_in_league:
        teams_dict[team["entry_name"]] = team
        teams_dict[team["entry_name"]]["player_data"] = get_player_data_for_team(team["entry"], player_data, live_data)
    """
    teams_dict = []
    for team in teams_in_league:
        new_team = team
        new_team["player_data"] = get_player_data_for_team(new_team["entry"], player_data, live_data)
        teams_dict.append(new_team)

    print("done")

    with open("data\json.json", 'w') as outfile:
        json.dump(teams_dict, outfile)

if __name__ == '__main__':
    main()