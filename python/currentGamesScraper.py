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

gamesXML = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml'
#gamesXML = 'testXML.xml'
obj = untangle.parse(gamesXML)
seasonYearA = int(obj.ss.gms['y'])
seasonYearB = seasonYearA + 1
seasonId = str(seasonYearA) + '-' + str(seasonYearB)
weekNum = int(obj.ss.gms['w'])
weekId = 'week' + str(weekNum)
prevWeekId = 'week' + str(weekNum - 1)
dbWeekPath = seasonId + '/' + weekId
week = root.child(dbWeekPath).get()
weekLen = len(week)
max = len(obj.ss.gms)
if prevWeekId == 0:
    firstWeek = True
startedGameArray = []
finishedGameArray = []

for it in range(0, max):
    startedGameArray.append(False)
    finishedGameArray.append(False)

while True:
    for i in range(0, max):
        gameId = obj.ss.gms.g[i]['gsis']
        homePoints = obj.ss.gms.g[i]['hs']
        awayPoints = obj.ss.gms.g[i]['vs']
        dbGamePath = dbWeekPath + '/' + gameId
        dbHomePath = dbGamePath + '/home'
        dbAwayPath = dbGamePath + '/away'
        root.child(dbHomePath).update({
            'points' : homePoints
        })
        root.child(dbAwayPath).update({
            'points' : awayPoints
        })
        if obj.ss.gms.g[i]['q'] == '1' and (not startedGameArray[i]):
            print 'gameStarted', gameId
            startedGameArray[i] = True
            gameStarted = root.child(dbGamePath).update({
                'started' : True
            })
        elif obj.ss.gms.g[i]['q'] == 'F' and (not finishedGameArray[i]):
            print 'gameFinished', gameId
            finishedGameArray[i] = True
            gameStarted = root.child(dbGamePath).update({
                'ended' : True
            })
            homePoints = obj.ss.gms.g[i]['hs']
            awayPoints = obj.ss.gms.g[i]['vs']
            dbPrevHomeWinsPath = dbHomePath + '/wins'
            dbPrevHomeLossPath = dbHomePath + '/losses'
            dbPrevAwayWinsPath = dbAwayPath + '/wins'
            dbPrevAwayLossPath = dbAwayPath + '/losses'
            if (homePoints > awayPoints):
                if firstWeek:
                    homeWins = 1
                    homeLosses = 0
                    awayWins = 0
                    awayLosses = 1
                else:
                    homeWins = root.child(dbPrevHomeWinsPath).get() + 1
                    homeLosses = root.child(dbPrevHomeLossPath)
                    awayWins = root.child(dbPrevAwayWinsPath)
                    awayLosses = root.child(dbPrevAwayLossPath).get() + 1
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
            elif (homePoints < awayPoints):
                if firstWeek:
                    homeWins = 0
                    homeLosses = 1
                    awayWins = 1
                    awayLosses = 0
                else:
                    homeWins = root.child(dbPrevHomeWinsPath).get()
                    homeLosses = root.child(dbPrevHomeLossPath) + 1
                    awayWins = root.child(dbPrevAwayWinsPath) + 1
                    awayLosses = root.child(dbPrevAwayLossPath).get()
                root.child(dbHomePath).update({
                    'points' : homePoints,
                    'winner' : False,
                    'wins' : homeWins,
                    'losses' : homeLosses
                })
                root.child(dbAwayPath).update({
                    'points' : awayPoints,
                    'winner' : True,
                    'wins' : awayWins,
                    'losses' : awayLosses
                })
    print 'sleeping'
    time.sleep(5)