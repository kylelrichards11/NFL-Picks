import json
from urllib.request import urlopen
import firebase_admin       # pylint: disable=unresolved-import
from firebase_admin import credentials
from firebase_admin import db
import os

YEAR = '2019-2020'
WEEK = 1

###############################################################################################
## NFL TO FIREBASE CONVERSIONS
###############################################################################################

# Maps from nfl id to firebase id
def make_id_map():
    home_team_ids = {}
    json_firebase_id_map = {}

    games_current = get_games_nfl()
    games_fb = fb_get_games(WEEK)

    for game in games_fb:
        home_team = games_fb[game]['home']['teamId']
        home_team_ids[home_team] = {'firebase_id': game}

    for game in games_current:
        home_team = games_current[game]['home']['abbr']

        # TODO: Fix abbr discrepency
        if home_team == 'JAC':
            home_team = 'JAX'

        home_team_ids[home_team]['json_id'] = game

    for k in home_team_ids:
        new_key = home_team_ids[k]['json_id']
        new_val = home_team_ids[k]['firebase_id']
        json_firebase_id_map[new_key] = new_val

    return json_firebase_id_map

###############################################################################################
## FIREBASE 
###############################################################################################

###############################################################################################
# SETUP

# Use credentials to gain access to firebase database
def fb_init():
    cred = credentials.Certificate("config.json")
    fb = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://nfl-picks-b5e4d.firebaseio.com'
    })

# Helper function to add to current value
def fb_increment(current_value, inc=1):
    return current_value + inc if current_value else inc

###############################################################################################
# READS

# Gets games dict for the desired week
def fb_get_games(week):
    week_games_ref = db.reference('/' + YEAR + '/weeks/week' + str(week) + '/games')
    return week_games_ref.get()

###############################################################################################
# WRITES

# Write that the game started
def fb_start_game(game):
    game_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game))
    game_ref.update({'started': True})

# Write a new score
def fb_update_score(game, score, team):
    score_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/' + team)
    score_ref.update({'points': str(score)})

# Write that the game ended, update team records, and update pick records
def fb_end_game(game, winner):
    home_id = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/home/teamID').get()
    away_id = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/away/teamID').get()

    if winner == 'tie':
        home_ties_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/home/ties')
        away_ties_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/away/ties')
        
        try:
            home_ties_ref.transaction(fb_increment)
            away_ties_ref.transaction(fb_increment)
        except db.TransactionError:
            print("Failed to commit transaction")

    else:
        winner_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/' + winner)
        wins_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/' + winner + '/wins')

        loser = 'away' if winner == 'home' else 'home'
        losses_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/' + loser + '/losses')

        winner_ref.update({'winner': True})

        try:
            wins_ref.transaction(fb_increment)
            losses_ref.transaction(fb_increment)
        except db.TransactionError:
            print("Failed to commit transaction")

    game_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game))
    game_ref.update({'started': True, 'ended': True})

    fb_update_pick_result()

def fb_update_record(team, result):
    

# Updates pick results for users
def fb_update_pick_result():
    ...

# TEMP Resets week data to all 0
def reset_week_games():
    games = fb_get_games(WEEK)
    for game in games:
        game_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game))
        game_ref.update({
            'started': False,
            'ended': False
        })

        home_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/home')
        away_ref = db.reference('/' + YEAR + '/weeks/week' + str(WEEK) + '/games/' + str(game) + '/away')
        teams_refs = (home_ref, away_ref)
        for team_ref in teams_refs:
            team_ref.update({
                'losses': 0,
                'wins': 0,
                'ties': 0,
                'winner': False,
                'points': "0",
            })

###############################################################################################
## NFL JSON FUNCTIONS
###############################################################################################

# Gets the current games from nfl
def get_games_nfl():
    games_json = urlopen('http://www.nfl.com/liveupdate/scores/scores.json')
    return json.loads(games_json.read())

# Gets game status and scores from nfl
def get_games_info():
    games = get_games_nfl()
    games_info = {}
    for game in games:
        games_info[game] = {}

        status = games[game]['qtr']
        if status == 'Final' or status == 'final overtime':
            games_info[game]['status'] = 'post'
        elif status is None:
            games_info[game]['status'] = 'pre'
        else:
            games_info[game]['status'] = 'playing'

        home_score = games[game]['home']['score']['T']
        if home_score is None:
            home_score = 0
        games_info[game]['home_score'] = home_score

        away_score = games[game]['away']['score']['T']
        if away_score is None:
            away_score = 0
        games_info[game]['away_score'] = away_score

    return games_info

# Determines if home or away team won the game (or tie)
def get_game_winner(game):
    if game['home_score'] > game['away_score']:
        return 'home'
    if game['home_score'] < game['away_score']:
        return 'away'
    return 'tie'

###############################################################################################
## WATCH GAMES
###############################################################################################

def watch_games_once(json_firebase_id_map):
    current_games = get_games_nfl()
    games_info = get_games_info()

    for game in games_info:
        fb_update_score(json_firebase_id_map[game], games_info[game]['home_score'], 'home')
        fb_update_score(json_firebase_id_map[game], games_info[game]['away_score'], 'away')
        if games_info[game]['status'] == 'playing':
            fb_start_game(json_firebase_id_map[game])
        elif games_info[game]['status'] == 'post':
            fb_end_game(json_firebase_id_map[game], get_game_winner(games_info[game]))

def watch_games(json_firebase_id_map, prev_games_info):
    current_games = get_games_nfl()
    games_info = get_games_info()

    for game in games_info:
        if games_info[game]['home_score'] != prev_games_info[game]['home_score']:
            fb_update_score(json_firebase_id_map[game], games_info[game]['home_score'], 'home')
        if games_info[game]['away_score'] != prev_games_info[game]['away_score']:
            fb_update_score(json_firebase_id_map[game], games_info[game]['away_score'], 'away')
        if games_info[game]['status'] != prev_games_info[game]['status']:
            if games_info[game]['status'] == 'playing':
                fb_start_game(json_firebase_id_map[game])
            elif games_info[game]['status'] == 'post':
                fb_end_game(json_firebase_id_map[game])

###############################################################################################
## MAIN
###############################################################################################

if __name__ == '__main__':

    fb_init()
    json_firebase_id_map = make_id_map()

    reset_week_games()

    games_info = get_games_info()
    watch_games_once(json_firebase_id_map)

    #games_info = watch_games(json_firebase_id_map, games_info)