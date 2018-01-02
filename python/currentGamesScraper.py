import untangle
import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})
root = db.reference()

#gamesXML = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml'
gamesXML = 'testXML.xml'
#gamesXML = 'http://www.nfl.com/ajax/scorestrip?season=2017&seasonType=REG&week=17'

obj = untangle.parse(gamesXML) #make an object from the XML import

seasonYearA = int(obj.ss.gms['y']) #the XML only contains the first year e.g. 2015, but the database uses 2015-2016
seasonYearB = seasonYearA + 1      #as the id, so we need to make that id with the second year
seasonId = str(seasonYearA) + '-' + str(seasonYearB)

weekNum = int(obj.ss.gms['w'])
weekId = 'week' + str(weekNum)

dbWeekPath = seasonId + '/' + weekId #make the db path for the week, ex: '2015-2016/week1'

numberOfGames = len(obj.ss.gms)

#determine if this is the first week of the season (matters for adding wins to previous win totals)
firstWeek = False
if weekNum == 1:
    firstWeek = True

#arrays that hold a boolean of whether the game corresponding to that index has started and finished respectively
startedGameArray = []
finishedGameArray = []

#fill each array with false
for it in range(0, numberOfGames):
    startedGameArray.append(False)
    finishedGameArray.append(False)

while True:
    for i in range(0, numberOfGames): #iterate through each game
        gameId = obj.ss.gms.g[i]['gsis']
        homeTeamId = obj.ss.gms.g[i]['h']
        awayTeamId = obj.ss.gms.g[i]['v']
        homePoints = obj.ss.gms.g[i]['hs']
        awayPoints = obj.ss.gms.g[i]['vs']
        dbGamePath = dbWeekPath + '/' + gameId
        dbHomePath = dbGamePath + '/home'
        dbAwayPath = dbGamePath + '/away'
        root.child(dbHomePath).update({ #update the home score
            'points' : homePoints
        })
        root.child(dbAwayPath).update({ #update the away score
            'points' : awayPoints
        })
        if obj.ss.gms.g[i]['q'] == '1' and (not startedGameArray[i]): #if the game has started (quarter=1)
            print 'gameStarted', gameId                               #and the game is not in the game started array
            startedGameArray[i] = True #add the game to the array
            gameStarted = root.child(dbGamePath).update({ #mark that the game has started in the database
                'started' : True
            })
        elif obj.ss.gms.g[i]['q'] == 'F' and (not finishedGameArray[i]): #if the game has ended and the game is not in the game finished array
            dbGameFinishedPath = dbGamePath + '/ended'
            prevFinished = root.child(dbGameFinishedPath).get()
            if not prevFinished: #if the database does not have the game as finished
                print 'gameFinished', gameId #mark that the game has ended in the database
                finishedGameArray[i] = True
                root.child(dbGamePath).update({
                    'ended' : True
                })
                homePoints = int(obj.ss.gms.g[i]['hs'])
                awayPoints = int(obj.ss.gms.g[i]['vs'])
                dbHomeTeamPath = seasonId + '/teams/' + homeTeamId
                dbAwayTeamPath = seasonId + '/teams/' + awayTeamId
                dbPrevHomeWinsPath = dbHomeTeamPath + '/currentWins'
                dbPrevHomeLossPath = dbHomeTeamPath + '/currentLosses'
                dbPrevHomeTiesPath = dbHomeTeamPath + '/currentTies'
                dbPrevAwayWinsPath = dbAwayTeamPath + '/currentWins'
                dbPrevAwayLossPath = dbAwayTeamPath + '/currentLosses'
                dbPrevAwayTiesPath = dbAwayTeamPath + '/currentTies'
                if (homePoints > awayPoints): #if the home team won
                    if firstWeek:
                        homeWins = 1
                        homeLosses = 0
                        homeTies = 0
                        awayWins = 0
                        awayLosses = 1
                        awayTies = 0
                    else:
                        homeWins = int(root.child(dbPrevHomeWinsPath).get()) + 1
                        homeLosses = root.child(dbPrevHomeLossPath).get()
                        homeTies = root.child(dbPrevHomeTiesPath).get()
                        awayWins = root.child(dbPrevAwayWinsPath).get()
                        awayLosses = int(root.child(dbPrevAwayLossPath).get()) + 1
                        awayTies = root.child(dbPrevAwayTiesPath).get()
                    root.child(dbHomePath).update({
                        'points' : homePoints,
                        'winner' : True,
                        'wins' : homeWins,
                        'losses' : homeLosses
                    })
                    root.child(dbAwayPath).update({
                        'points' : awayPoints,
                        'winner' : False,
                        'wins' : awayWins,
                        'losses' : awayLosses
                    })
                elif (homePoints < awayPoints): #if the away team won
                    if firstWeek:
                        homeWins = 0
                        homeLosses = 1
                        homeTies = 0
                        awayWins = 1
                        awayLosses = 0
                        awayTies = 0
                    else:
                        homeWins = root.child(dbPrevHomeWinsPath).get()
                        homeLosses = int(root.child(dbPrevHomeLossPath).get()) + 1
                        homeTies = root.child(dbPrevHomeTiesPath).get()
                        awayWins = int(root.child(dbPrevAwayWinsPath).get()) + 1
                        awayLosses = root.child(dbPrevAwayLossPath).get()
                        awayTies = root.child(dbPrevAwayTiesPath).get()
                    root.child(dbHomePath).update({
                        'points' : homePoints,
                        'winner' : False,
                        'wins' : homeWins,
                        'losses' : homeLosses,
                        'ties' : homeTies
                    })
                    root.child(dbAwayPath).update({
                        'points' : awayPoints,
                        'winner' : True,
                        'wins' : awayWins,
                        'losses' : awayLosses,
                        'ties' : awayTies
                    })
                else: #if the teams tied
                    if firstWeek:
                        homeWins = 0
                        homeLosses = 0
                        homeTies = 1
                        awayWins = 0
                        awayLosses = 0
                        awayTies = 1
                    else:
                        homeWins = root.child(dbPrevHomeWinsPath).get()
                        homeLosses = root.child(dbPrevHomeLossPath).get()
                        homeTies = int(root.child(dbPrevHomeTiesPath).get()) + 1
                        awayWins = root.child(dbPrevAwayWinsPath).get()
                        awayLosses = root.child(dbPrevAwayLossPath).get()
                        awayTies = int(root.child(dbPrevAwayTiesPath).get()) + 1
                    root.child(dbHomePath).update({
                        'points' : homePoints,
                        'winner' : False,
                        'wins' : homeWins,
                        'losses' : homeLosses,
                        'ties' : homeTies
                    })
                    root.child(dbAwayPath).update({
                        'points' : awayPoints,
                        'winner' : False,
                        'wins' : awayWins,
                        'losses' : awayLosses,
                        'ties' : awayTies
                    })
                prevHomePointsFor = int(root.child(dbHomeTeamPath + '/pointsFor').get()) #update team stats in database
                prevHomePointsAgainst = int(root.child(dbHomeTeamPath + '/pointsAgainst').get())
                prevAwayPointsFor = int(root.child(dbAwayTeamPath + '/pointsFor').get())
                prevAwayPointsAgainst = int(root.child(dbAwayTeamPath + '/pointsAgainst').get())
                root.child(dbHomeTeamPath).update({
                        'currentWins' : homeWins,
                        'currentLosses' : homeLosses,
                        'currentTies' : homeTies,
                        'pointsFor' : prevHomePointsFor + homePoints,
                        'pointsAgainst' : prevHomePointsAgainst + awayPoints
                    })
                root.child(dbAwayTeamPath).update({
                        'currentWins' : awayWins,
                        'currentLosses' : awayLosses,
                        'currentTies' : awayTies,
                        'pointsFor' : prevAwayPointsFor + awayPoints,
                        'pointsAgainst' : prevAwayPointsAgainst + homePoints
                    })
    print 'sleeping'
    time.sleep(5) #sleep for 5 seconds