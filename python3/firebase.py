import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Firebase():
    """ A class to interface between scripts and the realtime database for this project """
    def __init__(self):
        cred = credentials.Certificate("config.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://nfl-picks-b5e4d.firebaseio.com"
        })
        self.users = ["H3EI5DDrbldJEg2FxEk6N9oYnaf2", "wzht1HEeVZdTSw61qM6jS2j7TqN2"]

    def create_year(self, year_id):
        """ Creates a new year for the provided year id in the realtime database 
        
        Parameters
        ----------
        year_id : str - the year id

        Returns
        -------
        None
        """
        year_ref = db.reference(f"{year_id}")
        year_ref.set({
            "seasonInfo" : {
                "ended" : False,
                "seasonId" : year_id
            },
            "weeks" : {
                "week1": {"weekInfo": {"ended":False, "weekId": "week1"}},
                "week2": {"weekInfo": {"ended":False, "weekId": "week2"}},
                "week3": {"weekInfo": {"ended":False, "weekId": "week3"}},
                "week4": {"weekInfo": {"ended":False, "weekId": "week4"}},
                "week5": {"weekInfo": {"ended":False, "weekId": "week5"}},
                "week6": {"weekInfo": {"ended":False, "weekId": "week6"}},
                "week7": {"weekInfo": {"ended":False, "weekId": "week7"}},
                "week8": {"weekInfo": {"ended":False, "weekId": "week8"}},
                "week9": {"weekInfo": {"ended":False, "weekId": "week9"}},
                "week10": {"weekInfo": {"ended":False, "weekId": "week10"}},
                "week11": {"weekInfo": {"ended":False, "weekId": "week11"}},
                "week12": {"weekInfo": {"ended":False, "weekId": "week12"}},
                "week13": {"weekInfo": {"ended":False, "weekId": "week13"}},
                "week14": {"weekInfo": {"ended":False, "weekId": "week14"}},
                "week15": {"weekInfo": {"ended":False, "weekId": "week15"}},
                "week16": {"weekInfo": {"ended":False, "weekId": "week16"}},
                "week17": {"weekInfo": {"ended":False, "weekId": "week17"}}
            }
        })
        for user in self.users:
            user_year_ref = db.reference(f"users/{user}/seasons/{year_id}")
            user_year_ref.set({
                "correct": 0,
                "incorrect": 0,
                "weeks" : {
                    "week1": {"correct": 0, "incorrect":0, "weekId": "week1"},
                    "week2": {"correct": 0, "incorrect":0, "weekId": "week2"},
                    "week3": {"correct": 0, "incorrect":0, "weekId": "week3"},
                    "week4": {"correct": 0, "incorrect":0, "weekId": "week4"},
                    "week5": {"correct": 0, "incorrect":0, "weekId": "week5"},
                    "week6": {"correct": 0, "incorrect":0, "weekId": "week6"},
                    "week7": {"correct": 0, "incorrect":0, "weekId": "week7"},
                    "week8": {"correct": 0, "incorrect":0, "weekId": "week8"},
                    "week9": {"correct": 0, "incorrect":0, "weekId": "week9"},
                    "week10": {"correct": 0, "incorrect":0, "weekId": "week10"},
                    "week11": {"correct": 0, "incorrect":0, "weekId": "week11"},
                    "week12": {"correct": 0, "incorrect":0, "weekId": "week12"},
                    "week13": {"correct": 0, "incorrect":0, "weekId": "week13"},
                    "week14": {"correct": 0, "incorrect":0, "weekId": "week14"},
                    "week15": {"correct": 0, "incorrect":0, "weekId": "week15"},
                    "week16": {"correct": 0, "incorrect":0, "weekId": "week16"},
                    "week17": {"correct": 0, "incorrect":0, "weekId": "week17"}
                },
                "year": year_id
            })

    def create_game(self, year_id, week_id, game_id, game_info):
        """ Creates a game with the given id and info for the given year and week 
        
        Parameters
        ----------
        year_id : str - the year id for the given game

        week_id : str - the week id for the given game

        game_id : str - the id for the game

        game_info : dict - the information about the game to add

        Returns
        -------
        None
        """
        games_ref = db.reference(f"{year_id}/weeks/{week_id}/games")
        games_ref.update({game_id : game_info})