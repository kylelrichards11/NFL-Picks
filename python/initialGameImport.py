import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})

class Team():
    def __init__(self, city, name, wins, losses):
        self.city = city
        self.name = name
        self.wins = wins
        self.losses = losses

teams = { 
    "ARI" : Team("Arizona", "Cardinals", 0, 0),
    "ATL" : Team("Atlanta", "Falcons", 0, 0),
    "BAL" : Team("Baltimore", "Ravens", 0, 0),
    "BUF" : Team("Buffalo", "Bills", 0, 0),
    "CAR" : Team("Carolina", "Panthers", 0, 0),
    "CHI" : Team("Chicago", "Bears", 0, 0),
    "CIN" : Team("Cincinnati", "Bengals", 0, 0),
    "CLE" : Team("Cleveland", "Browns", 0, 0),
    "DAL" : Team("Dallas", "Cowboys", 0, 0),
    "DEN" : Team("Denver", "Broncos", 0, 0),
    "DET" : Team("Detroit", "Lions", 0, 0),
    "GB" : Team("Green Bay", "Packers", 0, 0),
    "HOU" : Team("Houston", "Texans", 0, 0),
    "IND" : Team("Indianapolis", "Colts", 0, 0),
    "JAC" : Team("Jacksonville", "Jaguars", 0, 0),
    "JAX" : Team("Jacksonville", "Jaguars", 0, 0),
    "KC" : Team("Kansas City", "Chiefs", 0, 0),
    "LA" : Team("Los Angeles", "Rams", 0, 0),
    "LAC" : Team("Los Angeles", "Chargers", 0, 0),
    "MIA" : Team("Miami", "Dolphins", 0, 0),
    "MIN" : Team("Minnesota", "Vikings", 0, 0),
    "NE" : Team("New England", "Patriots", 0, 0),
    "NYG" : Team("New York", "Giants", 0, 0),
    "NYJ" : Team("New York", "Jets", 0, 0),
    "NO" : Team("New Orleans", "Saints", 0, 0),
    "OAK" : Team("Oakland", "Raiders", 0, 0),
    "PHI" : Team("Philadelphia", "Eagles", 0, 0),
    "PIT" : Team("Pittsburgh", "Steelers", 0, 0),
    "SD" : Team("San Diego", "Chargers", 0, 0),
    "SEA" : Team("Seattle", "Seahawks", 0, 0),
    "SF" : Team("San Francisco", "49ers", 0, 0),
    "STL" : Team("Saint Louis", "Rams", 0, 0),
    "TB" : Team("Tampa Bay", "Buccaneers", 0, 0),
    "TEN" : Team("Tennessee", "Titans", 0, 0),
    "WAS" : Team("Washington", "Redskins", 0, 0)
}

monthsArray = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
seasonURLArray = [2015, 2016, 2017]
seasonDbArray = ["2015-2016", "2016-2017", "2017-2018"]




#obj = untangle.parse('http://www.nfl.com/liveupdate/scorestrip/ss.xml')
root = db.reference()

for i in range(0, 3):
    for team in teams.itervalues():
        team.wins = 0
        team.losses = 0
    for j in range(1, 18):
        gamesXML = 'http://www.nfl.com/ajax/scorestrip?season=' + str(seasonURLArray[i]) + '&seasonType=REG&week=' + str(j)
        obj = untangle.parse(gamesXML)
        max = len(obj.ss.gms)
        for k in range(0, max):
            teamA = obj.ss.gms.g[k]['v']
            teamH = obj.ss.gms.g[k]['h']
            xmlId = obj.ss.gms.g[k]['gsis']
            print teams[teamA].city, teams[teamA].name, "@", teams[teamH].city, teams[teamH].name
            dbPath = seasonDbArray[i] + '/week' + str(j) + '/' + str(xmlId)
            date = obj.ss.gms.g[k]['eid']
            month = monthsArray[int(date[4] + date[5])-1]
            day = date[6] + date[7]
            year = date[0] + date[1] + date[2] + date[3]
            time = obj.ss.gms.g[k]['t']
            finishedCheck = obj.ss.gms.g[k]['q']
            if finishedCheck == 'P' :
                finished = False
                started = False
                homeScore = ''
                awayScore = ''
            if finishedCheck == 'F' or finishedCheck == 'FO' :
                finished = True
                started = True
                homeScore = obj.ss.gms.g[k]['hs']
                awayScore = obj.ss.gms.g[k]['vs']
                homeWinner = False
                awayWinner = False
                if int(homeScore) > int(awayScore) :
                    homeWinner = True
                    teams[teamH].wins += 1
                    teams[teamA].losses += 1
                if int(awayScore) > int(homeScore) :
                    awayWinner = True
                    teams[teamH].losses += 1
                    teams[teamA].wins += 1
            newGame = root.child(dbPath).set({
                'home' : {
                    'city' : teams[teamH].city,
                    'name' : teams[teamH].name,
                    'winner' : homeWinner,
                    'losses' : teams[teamH].losses,
                    'wins' : teams[teamH].wins,
                    'points' : homeScore
                },
                'away' : {
                    'city' : teams[teamA].city,
                    'name' : teams[teamA].name,
                    'winner' : awayWinner,
                    'losses' : teams[teamA].losses,
                    'wins' : teams[teamA].wins,
                    'points' : awayScore
                },
                'date' : month + ' ' + day + ' ' + year,
                'time' : time,
                'gameId' : xmlId,
                'started' : started,
                'ended' : finished
            })