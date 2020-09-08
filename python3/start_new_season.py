import pandas as pd

from firebase import Firebase

YEAR = 2020
TEAMS = {
    "Arizona Cardinals" : {"city": "Arizona", "name": "Cardinals", "id": "ARI"},
    "Atlanta Falcons" : {"city": "Atlanta", "name": "Falcons", "id": "ATL"},
    "Baltimore Ravens" : {"city": "Baltimore", "name": "Ravens", "id": "BAL"},
    "Buffalo Bills" : {"city": "Buffalo", "name": "Bills", "id": "BUF"},
    "Carolina Panthers" : {"city": "Carolina", "name": "Panthers", "id": "CAR"},
    "Chicago Bears" : {"city": "Chicago", "name": "Bears", "id": "CHI"},
    "Cincinnati Bengals" : {"city": "Cincinnati", "name": "Bengals", "id": "CIN"},
    "Cleveland Browns" : {"city": "Cleveland", "name": "Browns", "id": "CLE"},
    "Dallas Cowboys" : {"city": "Dallas", "name": "Cowboys", "id": "DAL"},
    "Denver Broncos" : {"city": "Denver", "name": "Broncos", "id": "DEN"},
    "Detroit Lions" : {"city": "Detroit", "name": "Lions", "id": "DET"},
    "Green Bay Packers" : {"city": "Green Bay", "name": "Packers", "id": "GB"},
    "Houston Texans" : {"city": "Houston", "name": "Texans", "id": "HOU"},
    "Indianapolis Colts" : {"city": "Indianapolis", "name": "Colts", "id": "IND"},
    "Jacksonville Jaguars" : {"city": "Jacksonville", "name": "Jaguars", "id": "JAX"},
    "Kansas City Chiefs" : {"city": "Kansas City", "name": "Chiefs", "id": "KC"},
    "Las Vegas Raiders" : {"city": "Las Vegas", "name": "Raiders", "id": "LV"},
    "Los Angeles Chargers" : {"city": "Los Angeles", "name": "Chargers", "id": "LAC"},
    "Los Angeles Rams" : {"city": "Los Angeles", "name": "Rams", "id": "LA"},
    "Miami Dolphins" : {"city": "Miami", "name": "Dolphins", "id": "MIA"},
    "Minnesota Vikings" : {"city": "Minnesota", "name": "Vikings", "id": "MIN"},
    "New England Patriots" : {"city": "New England", "name": "Patriots", "id": "NE"},
    "New Orleans Saints" : {"city": "New Orleans", "name": "Saints", "id": "NO"},
    "New York Giants" : {"city": "New York", "name": "Giants", "id": "NYG"},
    "New York Jets" : {"city": "New York", "name": "Jets", "id": "NYJ"},
    "Philadelphia Eagles" : {"city": "Philadelphia", "name": "Eagles", "id": "PHI"},
    "Pittsburgh Steelers" : {"city": "Pittsburgh", "name": "Steelers", "id": "PIT"},
    "San Francisco 49ers" : {"city": "San Francisco", "name": "49ers", "id": "SF"},
    "Seattle Seahawks" : {"city": "Seattle", "name": "Seahawks", "id": "SEA"},
    "Tampa Bay Buccaneers" : {"city": "Tampa Bay", "name": "Buccaneers", "id": "TB"},
    "Tennessee Titans" : {"city": "Tennessee", "name": "Titans", "id": "TEN"},
    "Washington Football Team" : {"city": "Washington", "name": "Football Team", "id": "WAS"},
}

def get_schedule():
    """ Gets the schedule as a pandas dataframe from the csv file schedule.csv. This csv is a download from profootballreference.com 
    
    Parameters
    ----------
    None

    Returns
    -------
    pd.DataFrame - a dataframe of the schedule where each row is a game
    
    """
    schedule = pd.read_csv("schedule.csv", header=None, names=["week","weekday","date","away_team","away_pts","at","home_team","home_pts","game_time"])
    schedule["game_id"] = schedule.index
    schedule["game_id"] = schedule["game_id"].apply(lambda idx : YEAR*1000 + idx)
    return schedule

def process_date(date):
    """ Processes a string into the desired form for a date. It takes adds a 0 to the day if it is less than 10, and appends the year 
    
    Parameters
    ----------
    date : str - the string with a month name and day number

    Returns
    -------
    str - the string with the day appended to 0 if it is less than 10 and the year
    """
    month, day = date.split(' ')
    if len(day) == 1:
        day = f"0{day}"
    return f"{month} {day} {YEAR}"

def create_games(fb, schedule, year_id):
    """ Creates each game in the schedule to be added to the firebase database 
    
    Parameters
    ----------
    fb : Firebase - the instantiated firebase class

    schedule : pd.DataFrame - a dataframe of the schedule where each row is a game

    year_id : string - the id of the year

    Returns
    -------
    None
    """
    for _, row in schedule.iterrows():
        game_info = {
            "away" : {
                "city" : TEAMS[row["away_team"]]["city"],
                "losses": 0,
                "name" : TEAMS[row["away_team"]]["name"],
                "points": 0,
                "teamID" : TEAMS[row["away_team"]]["id"],
                "ties": 0,
                "winner": False,
                "wins": 0
            },
            "date": process_date(row["date"]),
            "ended": False,
            "gameId": row["game_id"],
            "home" : {
                "city" : TEAMS[row["home_team"]]["city"],
                "losses": 0,
                "name" : TEAMS[row["home_team"]]["name"],
                "points": 0,
                "teamID" : TEAMS[row["home_team"]]["id"],
                "ties": 0,
                "winner": False,
                "wins": 0
            },
            "started": False,
            "time": row["game_time"].split(' ')[0]
        }
        fb.create_game(year_id, f"week{row['week']}", row["game_id"], game_info)

def start_new_season():
    """ Adds all of the needed information to the firebase database to be able to start a new season. NOTE: You must put the season's schedule from profootballreference.com to the schedule.csv file
    
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    fb = Firebase()
    year_id = f"{YEAR}-{YEAR+1}"
    schedule = get_schedule()
    
    fb.create_year(year_id)
    create_games(fb, schedule, year_id)

if __name__ == "__main__":
    start_new_season()