import json
from urllib.request import urlopen
import firebase_admin       # pylint: disable=unresolved-import
from firebase_admin import credentials
from firebase_admin import db
import time
import copy
import logging

YEAR = '2019-2020'
WEEK = 3
finished_games = []
users = ('wzht1HEeVZdTSw61qM6jS2j7TqN2', 'H3EI5DDrbldJEg2FxEk6N9oYnaf2')

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
    week_games_ref = db.reference(f'{YEAR}/weeks/week{week}/games')
    return week_games_ref.get()

###############################################################################################
# WRITES

# Write that the game started
def fb_start_game(game):
    game_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}')
    game_ref.update({'started': True})

# Write a new score
def fb_update_score(game, score, team):
    score_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/{team}')
    score_ref.update({'points': str(score)})

def fb_update_record_all_weeks(results):
    for week in range(WEEK, 18):
        games = db.reference(f'{YEAR}/weeks/week{week}/games').get()
        set_count = 0
        for game in games:
            if set_count == 2:
                break
            for team in results:
                if games[game]['away']['teamId'] == team:
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/away/wins').set(results[team]['wins'])
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/away/losses').set(results[team]['losses'])
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/away/ties').set(results[team]['ties'])
                    set_count += 1
                elif games[game]['home']['teamId'] == team:
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/home/wins').set(results[team]['wins'])
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/home/losses').set(results[team]['losses'])
                    db.reference(f'{YEAR}/weeks/week{week}/games/{game}/home/ties').set(results[team]['ties'])
                    set_count += 1


# Write that the game ended, update team records, and update pick records
def fb_end_game(game, winner):
    home = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/home').get()
    away = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/away').get()
    
    home_id = home['teamId']
    away_id = away['teamId']

    home_wins = home['wins']
    home_losses = home['losses']
    home_ties = home['ties']

    away_wins = away['wins']
    away_losses = away['losses']
    away_ties = away['ties']


    if winner == 'tie':
        winner_name = 'tie'
        home_ties += 1
        away_ties += 1
    else:
        winner_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/{winner}')
        winner_ref.update({'winner': True})

        if winner == 'home':
            home_wins += 1
            away_losses += 1
            winner_name = home['city'] + ' ' + home['name']
        else:
            home_losses += 1
            away_wins += 1
            winner_name = away['city'] + ' ' + away['name']

    fb_update_record_all_weeks({
        home_id: {
            'wins': home_wins,
            'losses': home_losses,
            'ties': home_ties
        },
        away_id: {
            'wins': away_wins,
            'losses': away_losses,
            'ties': away_ties   
        }})

    game_ref = db.reference(f'/{YEAR}/weeks/week{WEEK}/games/{game}')
    game_ref.update({'started': True, 'ended': True})

    for user in users:
        pick_ref = db.reference(f'users/{user}/seasons/{YEAR}/weeks/week{WEEK}/{game}/pick')
        pick = pick_ref.get()

        if pick == winner_name:
            week_ref = db.reference(f'users/{user}/seasons/{YEAR}/weeks/week{WEEK}/correct')
            season_ref = db.reference(f'users/{user}/seasons/{YEAR}/correct')
            total_ref = db.reference(f'users/{user}/correct')

        else:
            week_ref = db.reference(f'users/{user}/seasons/{YEAR}/weeks/week{WEEK}/incorrect')
            season_ref = db.reference(f'users/{user}/seasons/{YEAR}/incorrect')
            total_ref = db.reference(f'users/{user}/incorrect')

        week_ref.transaction(fb_increment)
        season_ref.transaction(fb_increment)
        total_ref.transaction(fb_increment)


def fb_end_week(week=WEEK):
    week_ref = db.reference(f'/{YEAR}/weeks/week{week}/weekInfo')
    week_ref.update({'ended': True})


# TEMP Resets week data to all 0
def reset_week_games():
    games = fb_get_games(WEEK)
    for game in games:
        game_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}')
        game_ref.update({
            'started': False,
            'ended': False
        })

        home_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/home')
        away_ref = db.reference(f'{YEAR}/weeks/week{WEEK}/games/{game}/away')
        teams_refs = (home_ref, away_ref)
        for team_ref in teams_refs:
            team_ref.update({
                'losses': 0,
                'wins': 0,
                'ties': 0,
                'winner': False,
                'points': "",
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
        elif status is None or status == 'Pregame':
            games_info[game]['status'] = 'pre'
        else:
            games_info[game]['status'] = 'playing'

        home_score = games[game]['home']['score']['T']
        if home_score is None or games_info[game]['status'] == 'pre':
            home_score = ""
        games_info[game]['home_score'] = home_score

        away_score = games[game]['away']['score']['T']
        if away_score is None or games_info[game]['status'] == 'pre':
            away_score = ""
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
    games_info = remove_finished_games(get_games_info())
    if len(games_info) == 0:
        fb_end_week()
        print(f'Week {WEEK} ended')
        return games_info, False
    for game in games_info:
        try:
            if games_info[game]['home_score'] != prev_games_info[game]['home_score']:
                fb_update_score(json_firebase_id_map[game], games_info[game]['home_score'], 'home')
        except KeyError as e:
            print(e)
            print("game", game)
            print("game info", games_info)
        if games_info[game]['away_score'] != prev_games_info[game]['away_score']:
            fb_update_score(json_firebase_id_map[game], games_info[game]['away_score'], 'away')
        if games_info[game]['status'] != prev_games_info[game]['status']:
            if games_info[game]['status'] == 'playing':
                fb_start_game(json_firebase_id_map[game])
            elif games_info[game]['status'] == 'post':
                fb_end_game(json_firebase_id_map[game])
                finished_games.append(game)
    return games_info, True

def add_to_finished_games(game_info):
    for game in game_info:
        if game_info[game]['status'] == 'post':
            finished_games.append(game)

def remove_finished_games(game_info):
    temp_dict = copy.deepcopy(game_info)
    for game in temp_dict:
        if game in finished_games:
            game_info.pop(game)
    return game_info
        

###############################################################################################
## MAIN
###############################################################################################

if __name__ == '__main__':

    logging.info('Starting')

    fb_init()
    json_firebase_id_map = make_id_map()

    #reset_week_games()

    games_info = get_games_info()
    watch_games_once(json_firebase_id_map)
    add_to_finished_games(games_info)

    week_going = True

    while week_going:
        try:
            games_info, week_going = watch_games(json_firebase_id_map, games_info)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            logging.exception(e)
            time.sleep(40)
        time.sleep(20)
