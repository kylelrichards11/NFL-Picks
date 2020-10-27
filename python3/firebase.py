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

    def lock_game(self, year_id, week_id, game_id):
        """ Locks a game with the given id, year, and week by setting the started attribute to True
        
        Parameters
        ----------
        year_id : str - the year id for the given game

        week_id : str - the week id for the given game

        game_id : str - the id for the game

        Returns
        -------
        None
        """
        game_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}")
        game_ref.update({"started" : True})

    def unlock_game(self, year_id, week_id, game_id):
        """ Unlocks a game with the given id, year, and week by setting the started attribute to False
        
        Parameters
        ----------
        year_id : str - the year id for the given game

        week_id : str - the week id for the given game

        game_id : str - the id for the game

        Returns
        -------
        None
        """
        game_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}")
        game_ref.update({"started" : False})

    def end_game(self, year_id, week_id, game_id, away_score, home_score):
        """ Ends a game by setting the ended attribute to true and filling in the scores, winner, loser attributes 
        
        Parameters
        ----------
        year_id : str - the year of the game

        week_id : str - the week of the game

        game_id : int - the id of the game

        away_score : int - the number of points the away team scored

        home_score : int - the number of points the home team scored

        Returns
        -------
        None
        """
        game_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}")
        game_ref.update({
            "started" : True,
            "ended" : True
        })

        game = game_ref.get()

        tie = away_score == home_score
        away_win = away_score > home_score
        home_win = away_score < home_score

        winner_key = "away" if away_win else "home"
        winner_name = None if tie else f"{game[winner_key]['city']} {game[winner_key]['name']}"

        away_records = {
            "losses": game["away"]["losses"],
            "ties": game["away"]["ties"],
            "wins": game["away"]["wins"],
        }

        home_records = {
            "losses": game["home"]["losses"],
            "ties": game["home"]["ties"],
            "wins": game["home"]["wins"],
        }

        away_record_key = "wins" if away_win else "losses" if home_win else "ties"
        home_record_key = "wins" if home_win else "losses" if away_win else "ties"
        away_records[away_record_key] = away_records[away_record_key] + 1
        home_records[home_record_key] = home_records[home_record_key] + 1
        
        away_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/away")
        away_ref.update({
            "winner" : away_win,
            "points" : away_score,
        })
        self.set_team_record(year_id, week_id, game["away"]["name"], away_records["wins"], away_records["losses"], away_records["ties"])

        home_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/home")
        home_ref.update({
            "winner" : home_win,
            "points" : home_score,
        })
        self.set_team_record(year_id, week_id, game["home"]["name"], home_records["wins"], home_records["losses"], home_records["ties"])

        for user in self.users:
            user_pick = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/{game_id}/pick").get()
            if user_pick == winner_name:
                self.inc_user_correct(user, year_id, week_id)
            else:
                self.inc_user_incorrect(user, year_id, week_id)

    def end_week(self, year_id, week_id):
        """ Ends the week in the given year by setting the ended attribute to True 
        
        Parameters
        ----------
        year_id : str - the id of the year

        week_id : str - the id of the week

        Returns
        -------
        None
        """
        db.reference(f"{year_id}/weeks/{week_id}/weekInfo/ended").set(True)


    def inc_user_correct(self, user, year_id, week_id):
        """ Increments the user's correct number for overall, the year, and the week 
        
        Parameters
        ----------
        user : str - the user's id

        year_id : str - the year to increment

        week_id : str - the week to increment

        Returns
        -------
        None
        """
        user_correct_ref = db.reference(f"users/{user}/correct")
        user_correct_num = user_correct_ref.get() + 1
        user_correct_ref.set(user_correct_num)

        year_correct_ref = db.reference(f"users/{user}/seasons/{year_id}/correct")
        year_correct_num = year_correct_ref.get() + 1
        year_correct_ref.set(year_correct_num)

        week_correct_ref = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/correct")
        week_correct_num = week_correct_ref.get() + 1
        week_correct_ref.set(week_correct_num)

    def inc_user_incorrect(self, user, year_id, week_id):
        """ Increments the user's incorrect number for overall, the year, and the week 
        
        Parameters
        ----------
        user : str - the user's id

        year_id : str - the year to increment

        week_id : str - the week to increment

        Returns
        -------
        None
        """
        user_incorrect_ref = db.reference(f"users/{user}/incorrect")
        user_incorrect_num = user_incorrect_ref.get() + 1
        user_incorrect_ref.set(user_incorrect_num)

        year_incorrect_ref = db.reference(f"users/{user}/seasons/{year_id}/incorrect")
        year_incorrect_num = year_incorrect_ref.get() + 1
        year_incorrect_ref.set(year_incorrect_num)

        week_incorrect_ref = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/incorrect")
        week_incorrect_num = week_incorrect_ref.get() + 1
        week_incorrect_ref.set(week_incorrect_num)

    def dec_user_correct(self, user, year_id, week_id):
        """ Decrements the user's correct number for overall, the year, and the week 
        
        Parameters
        ----------
        user : str - the user's id

        year_id : str - the year to decrement

        week_id : str - the week to decrement

        Returns
        -------
        None
        """
        user_correct_ref = db.reference(f"users/{user}/correct")
        user_correct_num = user_correct_ref.get() - 1
        user_correct_ref.set(user_correct_num)

        year_correct_ref = db.reference(f"users/{user}/seasons/{year_id}/correct")
        year_correct_num = year_correct_ref.get() - 1
        year_correct_ref.set(year_correct_num)

        week_correct_ref = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/correct")
        week_correct_num = week_correct_ref.get() - 1
        week_correct_ref.set(week_correct_num)

    def dec_user_incorrect(self, user, year_id, week_id):
        """ Decrements the user's incorrect number for overall, the year, and the week 
        
        Parameters
        ----------
        user : str - the user's id

        year_id : str - the year to decrement

        week_id : str - the week to decrement

        Returns
        -------
        None
        """
        user_incorrect_ref = db.reference(f"users/{user}/incorrect")
        user_incorrect_num = user_incorrect_ref.get() - 1
        user_incorrect_ref.set(user_incorrect_num)

        year_incorrect_ref = db.reference(f"users/{user}/seasons/{year_id}/incorrect")
        year_incorrect_num = year_incorrect_ref.get() - 1
        year_incorrect_ref.set(year_incorrect_num)

        week_incorrect_ref = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/incorrect")
        week_incorrect_num = week_incorrect_ref.get() - 1
        week_incorrect_ref.set(week_incorrect_num)

    def make_pick(self, user, year_id, week_id, game_id, pick):
        """ Sets the pick for a user 
        
        Parameters
        ----------
        user : str - the user's firebase id

        year_id : str - the year of the game to pick

        week_id : str - the week of the game to pick

        game_id : str - the id of the game to pick

        pick : str - the team to choose
        
        Returns
        -------
        None
        """
        db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/{game_id}").set({
            "pick": pick
        })

    def set_team_record(self, year_id, current_week_id, team_name, team_wins, team_losses, team_ties):
        current_week_num = int(current_week_id[4:])
        for week_num in range(current_week_num, 18):
            week_id = f"week{week_num}"
            games = db.reference(f"{year_id}/weeks/{week_id}/games").get()
            for game in games:
                if games[game]["away"]["name"] == team_name:
                    db.reference(f"{year_id}/weeks/{week_id}/games/{game}/away").update({
                        "losses": team_losses,
                        "ties": team_ties,
                        "wins": team_wins
                    })
                    break
                if games[game]["home"]["name"] == team_name:
                    db.reference(f"{year_id}/weeks/{week_id}/games/{game}/home").update({
                        "losses": team_losses,
                        "ties": team_ties,
                        "wins": team_wins
                    })
                    break

    def set_score(self, year_id, week_id, game_id, away_score=None, home_score=None):
        """ Sets the score of a game. If away_score and home_score are None, then they are set as blank scores
        
        Parameters
        ----------
        year_id : str - the year of the game to pick

        week_id : str - the week of the game to pick

        game_id : str - the id of the game to pick

        away_score : int or None - the score of the away team
        
        home_score : int or None - the score of the home team

        Returns
        -------
        None
        """
        away_score = '' if away_score is None else away_score
        home_score = '' if home_score is None else home_score

        away_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/away")
        home_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/home")

        away_ref.update({
            "points" : away_score,
        })
        home_ref.update({
            "points" : home_score,
        })

    def get_week_games(self, year_id, week_id):
        """ Gets a list of game ids for the given week in the given year

        Parameters
        ----------
        year_id : str - the year of the desired week

        week_id : str - the desired week

        Returns
        -------
        list of ints - a list of the game ids for that week
        """
        games_ref = db.reference(f"{year_id}/weeks/{week_id}/games/")
        return list(games_ref.get().keys())

    def undo_end_game(self, year_id, week_id, game_id):
        """ Undoes an end_game in case incorrect information was entered 
        
        Parameters
        ----------
        year_id : str - the year of the game to undo

        week_id : str - the week of the game to undo

        game_id : str - the id of the game to undo

        Returns
        -------
        None
        """
        game_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}")
        game_ref.update({
            "started" : False,
            "ended" : False
        })

        game = game_ref.get()

        away_score = game["away"]["points"]
        home_score = game["home"]["points"]

        tie = away_score == home_score
        away_win = away_score > home_score
        home_win = away_score < home_score

        winner_key = "away" if away_win else "home"
        winner_name = None if tie else f"{game[winner_key]['city']} {game[winner_key]['name']}"


        if away_win:
            self.set_team_record(year_id, week_id, game["away"]["name"], game["away"]["wins"] - 1, game["away"]["losses"], game["away"]["ties"])
            self.set_team_record(year_id, week_id, game["home"]["name"], game["home"]["wins"], game["home"]["losses"] - 1, game["home"]["ties"])
        elif home_win:
            self.set_team_record(year_id, week_id, game["away"]["name"], game["away"]["wins"], game["away"]["losses"] - 1, game["away"]["ties"])
            self.set_team_record(year_id, week_id, game["home"]["name"], game["home"]["wins"] - 1, game["home"]["losses"], game["home"]["ties"])
        else:
            self.set_team_record(year_id, week_id, game["away"]["name"], game["away"]["wins"], game["away"]["losses"], game["away"]["ties"] - 1)
            self.set_team_record(year_id, week_id, game["home"]["name"], game["home"]["wins"], game["home"]["losses"], game["home"]["ties"] - 1)

        away_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/away")
        home_ref = db.reference(f"{year_id}/weeks/{week_id}/games/{game_id}/home")

        away_ref.update({
            "points": "",
            "winner": False
        })
        home_ref.update({
            "points": "",
            "winner": False
        })
        for user in self.users:
            user_pick = db.reference(f"users/{user}/seasons/{year_id}/weeks/{week_id}/{game_id}/pick").get()
            if user_pick == winner_name:
                self.dec_user_correct(user, year_id, week_id)
            else:
                self.dec_user_incorrect(user, year_id, week_id)


if __name__ == "__main__":
    fb = Firebase()