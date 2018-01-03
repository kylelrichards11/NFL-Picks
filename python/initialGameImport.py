import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})
root = db.reference()


class Team():
    def __init__(self, city, name, wins, losses, ties):
        self.city = city
        self.name = name
        self.wins = wins
        self.losses = losses
        self.ties = ties

#dictionary that keeps track of team names, wins, losses, and ties. This gets reset for each season
teams = { 
    "ARI" : Team("Arizona", "Cardinals", 0, 0, 0),
    "ATL" : Team("Atlanta", "Falcons", 0, 0, 0),
    "BAL" : Team("Baltimore", "Ravens", 0, 0, 0),
    "BUF" : Team("Buffalo", "Bills", 0, 0, 0),
    "CAR" : Team("Carolina", "Panthers", 0, 0, 0),
    "CHI" : Team("Chicago", "Bears", 0, 0, 0),
    "CIN" : Team("Cincinnati", "Bengals", 0, 0, 0),
    "CLE" : Team("Cleveland", "Browns", 0, 0, 0),
    "DAL" : Team("Dallas", "Cowboys", 0, 0, 0),
    "DEN" : Team("Denver", "Broncos", 0, 0, 0),
    "DET" : Team("Detroit", "Lions", 0, 0, 0),
    "GB" : Team("Green Bay", "Packers", 0, 0, 0),
    "HOU" : Team("Houston", "Texans", 0, 0, 0),
    "IND" : Team("Indianapolis", "Colts", 0, 0, 0),
    "JAC" : Team("Jacksonville", "Jaguars", 0, 0, 0),
    "JAX" : Team("Jacksonville", "Jaguars", 0, 0, 0),
    "KC" : Team("Kansas City", "Chiefs", 0, 0, 0),
    "LA" : Team("Los Angeles", "Rams", 0, 0, 0),
    "LAC" : Team("Los Angeles", "Chargers", 0, 0, 0),
    "MIA" : Team("Miami", "Dolphins", 0, 0, 0),
    "MIN" : Team("Minnesota", "Vikings", 0, 0, 0),
    "NE" : Team("New England", "Patriots", 0, 0, 0),
    "NYG" : Team("New York", "Giants", 0, 0, 0),
    "NYJ" : Team("New York", "Jets", 0, 0, 0),
    "NO" : Team("New Orleans", "Saints", 0, 0, 0),
    "OAK" : Team("Oakland", "Raiders", 0, 0, 0),
    "PHI" : Team("Philadelphia", "Eagles", 0, 0, 0),
    "PIT" : Team("Pittsburgh", "Steelers", 0, 0, 0),
    "SD" : Team("San Diego", "Chargers", 0, 0, 0),
    "SEA" : Team("Seattle", "Seahawks", 0, 0, 0),
    "SF" : Team("San Francisco", "49ers", 0, 0, 0),
    "STL" : Team("Saint Louis", "Rams", 0, 0, 0),
    "TB" : Team("Tampa Bay", "Buccaneers", 0, 0, 0),
    "TEN" : Team("Tennessee", "Titans", 0, 0, 0),
    "WAS" : Team("Washington", "Redskins", 0, 0, 0)
}

monthsArray = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
seasonURLArray = [2015, 2016, 2017]
seasonDbArray = ["2015-2016", "2016-2017", "2017-2018"]

for i in range(0, 3): #loop through 3 seasons
    root.child(seasonDbArray[i] + '/seasonInfo').update({
        'ended' : True,
        'seasonId' : seasonDbArray[i]
    })
    for team in teams.itervalues(): #reset dictionary
        team.wins = 0
        team.losses = 0
        team.ties = 0
    for j in range(1, 18): #loop through 17 weeks
        gamesXML = 'http://www.nfl.com/ajax/scorestrip?season=' + str(seasonURLArray[i]) + '&seasonType=REG&week=' + str(j) #get XML from NFLGameCenter
        obj = untangle.parse(gamesXML) #get object from XML
        numberOfGames = len(obj.ss.gms)
        weekId = 'week' + str(j)
        dbWeekPath = seasonDbArray[i] + '/weeks/' + weekId
        root.child(dbWeekPath + '/weekInfo').update({
            'weekId' : weekId,
            'ended' : True
        })
        for k in range(0, numberOfGames): #loop through games in week
            awayTeamId = obj.ss.gms.g[k]['v']
            homeTeamId = obj.ss.gms.g[k]['h']
            gameId = obj.ss.gms.g[k]['gsis'] #get the id assigned to the game by the XML
            print teams[awayTeamId].city, teams[awayTeamId].name, "@", teams[homeTeamId].city, teams[homeTeamId].name
            dbPath = dbWeekPath + '/games/' + str(gameId)
            date = obj.ss.gms.g[k]['eid']
            month = monthsArray[int(date[4] + date[5])-1] #get month from date
            day = date[6] + date[7] #get day from date
            year = date[0] + date[1] + date[2] + date[3] #get year from date
            time = obj.ss.gms.g[k]['t']
            gameStatus = obj.ss.gms.g[k]['q'] #check whether game has started or finished
            if gameStatus == 'P' : #if the game has not yet started
                finished = False
                started = False
                homeScore = ''
                awayScore = ''
            if gameStatus == 'F' or gameStatus == 'FO': #if the game has finished
                finished = True
                started = True
                homeScore = obj.ss.gms.g[k]['hs']
                awayScore = obj.ss.gms.g[k]['vs']
                homeWinner = False
                awayWinner = False
                if int(homeScore) > int(awayScore): #if the home team won
                    homeWinner = True
                    teams[homeTeamId].wins += 1
                    teams[awayTeamId].losses += 1
                elif int(awayScore) > int(homeScore): #if the away team won
                    awayWinner = True
                    teams[homeTeamId].losses += 1
                    teams[awayTeamId].wins += 1
                else: #if there was a tie
                    teams[homeTeamId].ties += 1
                    teams[awayTeamId].ties += 1
            root.child(dbPath).set({ #add game to firebase
                'home' : {
                    'teamId' : homeTeamId,
                    'city' : teams[homeTeamId].city,
                    'name' : teams[homeTeamId].name,
                    'winner' : homeWinner,
                    'wins' : teams[homeTeamId].wins,
                    'losses' : teams[homeTeamId].losses,
                    'ties' : teams[homeTeamId].ties,
                    'points' : homeScore
                },
                'away' : {
                    'teamId' : awayTeamId,
                    'city' : teams[awayTeamId].city,
                    'name' : teams[awayTeamId].name,
                    'winner' : awayWinner,
                    'wins' : teams[awayTeamId].wins,
                    'losses' : teams[awayTeamId].losses,
                    'ties' : teams[awayTeamId].ties,
                    'points' : awayScore
                },
                'date' : month + ' ' + day + ' ' + year,
                'time' : time,
                'gameId' : gameId,
                'started' : started,
                'ended' : finished
            })