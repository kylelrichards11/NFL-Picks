import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

teams = { 
    "Arizona" : "Arizona Cardinals",
    "Cardinals" : "Arizona Cardinals",
    "Atlanta" : "Atlanta Falcons",
    "Falcons" : "Atlanta Falcons",
    "Baltimore" : "Baltimore Ravens",
    "Ravens" : "Baltimore Ravens",
    "Buffalo" : "Buffalo Bills",
    "Bills" : "Buffalo Bills",
    "Carolina" : "Carolina Panthers",
    "Panthers" : "Carolina Panthers",
    "Chicago" : "Chicago Bears",
    "Bears" : "Chicago Bears",
    "Cincinnati" : "Cincinnati Bengals",
    "Bengals" : "Cincinnati Bengals",
    "Cleveland" : "Cleveland Browns",
    "Browns" : "Cleveland Browns",
    "Dallas" : "Dallas Cowboys",
    "Cowboys" : "Dallas Cowboys",
    "Denver" : "Denver Broncos",
    "Broncos" : "Denver Broncos",
    "Detroit" : "Detroit Lions",
    "Lions" : "Detroit Lions",
    "Green Bay" : "Green Bay Packers",
    "Packers" : "Green Bay Packers",
    "Houston" : "Houston Texans",
    "Texans" : "Houston Texans",
    "Indianapolis" : "Indianapolis Colts",
    "Colts" : "Indianapolis Colts",
    "Jacksonville" : "Jacksonville Jaguars",
    "Jaguars" : "Jacksonville Jaguars",
    "Kansas" : "Kansas City Chiefs",
    "Kansas City" : "Kansas City Chiefs",
    "Chiefs" : "Kansas City Chiefs",
    "Miami" : "Miami Dolphins",
    "Dolphins" : "Miami Dolphins",
    "Minnesota" : "Minnesota Vikings",
    "Vikings" : "Minnesota Vikings",
    "New England" : "New England Patriots",
    "Patriots" : "New England Patriots",
    "Giants" : "New York Giants",
    "Jets" : "New York Jets",
    "New Orleans" : "New Orleans Saints",
    "Saints" : "New Orleans Saints",
    "Oakland" : "Oakland Raiders",
    "Raiders" : "Oakland Raiders",
    "Philadelphia" : "Philadelphia Eagles",
    "Eagles" : "Philadelphia Eagles",
    "Pittsburgh" : "Pittsburgh Steelers",
    "Steelers" : "Pittsburgh Steelers",
    "San Diego" : "San Diego Chargers",
    "Seattle" : "Seattle Seahawks",
    "Seahawks" : "Seattle Seahawks",
    "San Francisco" : "San Francisco 49ers",
    "49ers" : "San Francisco 49ers",
    "Saint Louis" : "Saint Louis Rams",
    "St. Louis" : "Saint Louis Rams",
    "Tampa" : "Tampa Bay Buccaneers",
    "Tampa Bay" : "Tampa Bay Buccaneers",
    "Buccaneers" : "Tampa Bay Buccaneers",
    "Tennessee" : "Tennessee Titans",
    "Titans" : "Tennessee Titans",
    "Washington" : "Washington Redskins",
    "Redskins" : "Washington Redskins"
}

cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})

root = db.reference()
obj = untangle.parse('picks.xml')

kyleUID = 'H3EI5DDrbldJEg2FxEk6N9oYnaf2'
dadUID = 'wzht1HEeVZdTSw61qM6jS2j7TqN2'

UIDs = [kyleUID, dadUID]
userNames = ['Kyle', 'Dad']
usersNum = len(UIDs)
gameIds = [56502, 56900, 57233]
gameIdsIndex = 0

max = len(obj.root)

for user in range(0, usersNum):
    print 'user' + str(user)
    prevWeek = 0
    prevSeason = 0
    weekCorrectCount = 0
    weekIncorrectCount = 0
    seasonCorrect = 0
    seasonIncorrect = 0
    gameIdsIndex = 0
    for i in range(0, max):
        if prevSeason != obj.root.row[i]['Season']:
            dbSeasonUserPath = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season']
            newSeason = root.child(dbSeasonUserPath).update({
                'year' : obj.root.row[i]['Season']
            })
            print obj.root.row[i]['Season']
            if prevSeason != 0:
                dbPrevSeasonUserPath = 'users/' + UIDs[user] + '/seasons/' + prevSeason
                newSeasonCorrectIncorrect = root.child(dbPrevSeasonUserPath).update({
                    'correct' : seasonCorrect,
                    'incorrect' : seasonIncorrect
                })
            seasonCorrect = 0
            seasonIncorrect = 0
            gameId = gameIds[gameIdsIndex]
            gameIdsIndex += 1
            prevSeason = obj.root.row[i]['Season']
        if prevWeek != obj.root.row[i]['Week']:
            prevWeek = obj.root.row[i]['Week']
            dbPathWeekId = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'])
            weekId = 'week' + str(obj.root.row[i]['Week'])
            newWeekId = root.child(dbPathWeekId).update({
                'weekId' : weekId
            })
            print weekId
            firstGameInWeek = i
            dbPathWeek = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'])
            week = root.child(dbPathWeek).get()
            gamesInWeek = len(week)
            lastGameInWeek = firstGameInWeek + gamesInWeek
            for j in range (0, gamesInWeek):
                gameId += 1
                if gameId == 57241 and weekId == 'week1': #dealing with buccaneers dolphins postponed game
                    gameId = 57242
                if gameId == 57242 and weekId == 'week11':
                    gameId = 57381
                elif gameId == 57381:
                    gameId = 57241
                dbPathHomeCity = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'] + '/games/' + str(gameId) + '/home/city')
                dbPathHomeName = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'] + '/games/' + str(gameId) + '/home/name')
                dbPathAwayCity = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'] + '/games/' + str(gameId) + '/away/city')
                dbPathAwayName = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'] + '/games/' + str(gameId) + '/away/name')
                homeCity = root.child(dbPathHomeCity).get()
                homeName = root.child(dbPathHomeName).get()
                homeBoth = homeCity + ' ' + homeName
                awayCity = root.child(dbPathAwayCity).get()
                awayName = root.child(dbPathAwayName).get()
                awayBoth = awayCity + ' ' + awayName
                for k in range(firstGameInWeek, lastGameInWeek):
                    userName = userNames[user]
                    userPick = obj.root.row[k][userName]
                    if userPick == "St. Louis":
                        userPick = "Saint Louis"
                    elif userPick == "Rams":
                        if obj.root.row[i]['Season'] == '2015-2016':
                            userPick = "Saint Louis Rams"
                        else:
                            userPick = "Los Angeles Rams"
                    elif userPick == "Chargers":
                        if obj.root.row[i]['Season'] == '2017-2018':
                            userPick = "Los Angeles Chargers"
                        else:
                            userPick = "San Diego Chargers"
                    if userPick in homeBoth or userPick in awayBoth:
                        dbSetUserPickPath = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/' + str(gameId)
                        if userPick == homeBoth or userPick == awayBoth:
                            newPick = root.child(dbSetUserPickPath).set({
                                'pick' : userPick
                            })
                        else:
                            userPick = teams[userPick]
                            newPick = root.child(dbSetUserPickPath).set({
                                'pick' : userPick
                            })
                            print gameId
                        if userPick == homeBoth:
                            dbPathHome = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/games/' + str(gameId) + '/home/winner'
                            correct = root.child(dbPathHome).get()
                            if correct:
                                weekCorrectCount += 1
                            else:
                                weekIncorrectCount += 1
                        elif userPick == awayBoth:
                            dbPathAway = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/games/' + str(gameId) + '/away/winner'
                            correct = root.child(dbPathAway).get()
                            if correct:
                                weekCorrectCount += 1
                            else:
                                weekIncorrectCount += 1
            dbPathUserWeek = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/' + weekId
            newCorrect = root.child(dbPathUserWeek).update({
                'correct' : weekCorrectCount
            })
            newIncorrecrt = root.child(dbPathUserWeek).update({
                'incorrect' : weekIncorrectCount
            })
            seasonCorrect += weekCorrectCount
            seasonIncorrect += weekIncorrectCount
            weekCorrectCount = 0
            weekIncorrectCount = 0