import firebase_admin       # pylint: disable=unresolved-import
from firebase_admin import credentials
from firebase_admin import db

# This script recounts each user's pick record

users = ['wzht1HEeVZdTSw61qM6jS2j7TqN2', 'H3EI5DDrbldJEg2FxEk6N9oYnaf2']

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

###############################################################################################
## MAIN
###############################################################################################
if __name__ == "__main__":
    fb_init()

    for user in users:
        total_correct = 0
        total_incorrect = 0
        seasons_ref = db.reference(f'/users/{user}/seasons')
        seasons = seasons_ref.get()
        for season in seasons:
            season_correct = 0
            season_incorrect = 0
            results_ref = db.reference(f'{season}')
            results = results_ref.get()
            for week in seasons[season]['weeks']:
                week_correct = 0
                week_incorrect = 0
                for game in seasons[season]['weeks'][week]:
                    if not (game == 'correct' or game == 'incorrect' or game == 'weekId'):
                        pick = seasons[season]['weeks'][week][game]['pick']
                        game_results = results['weeks'][week]['games'][game]
                        homeName = game_results['home']['city'] + " " + game_results['home']['name']
                        if game_results['ended']:
                            if pick == homeName:
                                if game_results['home']['winner']:
                                    total_correct += 1
                                    season_correct += 1
                                    week_correct += 1
                                else:
                                    total_incorrect += 1
                                    season_incorrect += 1
                                    week_incorrect += 1
                            elif game_results['away']['winner']:
                                total_correct += 1
                                season_correct += 1
                                week_correct += 1
                            else:
                                total_incorrect += 1
                                season_incorrect += 1
                                week_incorrect += 1
                week_ref = db.reference(f'users/{user}/seasons/{season}/weeks/{week}')
                week_ref.update({'correct': week_correct})
                week_ref.update({'incorrect': week_incorrect})
                print(f'{season} {week} {week_correct}-{week_incorrect}')
            season_ref = db.reference(f'users/{user}/seasons/{season}')
            season_ref.update({'correct': season_correct})
            season_ref.update({'incorrect': season_incorrect})
        total_ref = db.reference(f'users/{user}')
        total_ref.update({'correct': total_correct})
        total_ref.update({'incorrect': total_incorrect})