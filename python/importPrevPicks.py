import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#dictionary that translates either just city or just name to city and name
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

#firebase authentication
cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})

root = db.reference()
obj = untangle.parse('picks.xml')

kyleUID = 'H3EI5DDrbldJEg2FxEk6N9oYnaf2'
dadUID = 'wzht1HEeVZdTSw61qM6jS2j7TqN2'
sampleUID = '9OMOuqYE6Ncra2bMBptPpMnYwNt2'

#UIDs = [kyleUID, dadUID] #an array of our user ids
UIDs = [sampleUID]
#userNames = ['Kyle', 'Dad']
userNames = ['Kyle']
usersNum = len(UIDs) #number of users

gameIds = [56169, 56502, 56900, 57233] #this array holds the number before the first game id of each season
gameIdsIndex = 0

games = len(obj.root) #the number of games we are looking through

for user in range(0, usersNum): #for each user
    print userNames[user]
    totalCorrect = 0 #reset cumulative stats
    totalIncorrect = 0
    prevWeek = 0
    prevSeason = 0
    weekCorrectCount = 0
    weekIncorrectCount = 0
    seasonCorrect = 0
    seasonIncorrect = 0
    gameIdsIndex = 0
    for i in range(0, games): # for each game
        if prevSeason != obj.root.row[i]['Season']: #if this game's season is different than the last game's season
            seasonId = obj.root.row[i]['Season'] #update the season id
            dbSeasonUserPath = 'users/' + UIDs[user] + '/seasons/' + seasonId
            root.child(dbSeasonUserPath).update({ #write season year to the database
                'year' : obj.root.row[i]['Season']
            })
            print obj.root.row[i]['Season']
            if prevSeason != 0: #if there was a previous season
                dbPrevSeasonUserPath = 'users/' + UIDs[user] + '/seasons/' + prevSeason
                newSeasonCorrectIncorrect = root.child(dbPrevSeasonUserPath).update({ #write stats to database
                    'correct' : seasonCorrect,
                    'incorrect' : seasonIncorrect
                })
            totalCorrect += seasonCorrect #update the user's total correct and incorrect
            totalIncorrect += seasonIncorrect
            seasonCorrect = 0 #reset stats
            seasonIncorrect = 0
            gameId = gameIds[gameIdsIndex] #get the starting game id for this season
            gameIdsIndex += 1
            prevSeason = obj.root.row[i]['Season'] #set previous season to this season
        if prevWeek != obj.root.row[i]['Week']: #if this game's week is different than the last game's week
            prevWeek = obj.root.row[i]['Week'] #set previous week to this week
            dbPathWeekId = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week'])
            weekId = 'week' + str(obj.root.row[i]['Week']) #get weekId and write to database
            newWeekId = root.child(dbPathWeekId).update({
                'weekId' : weekId
            })
            print weekId
            firstGameInWeek = i #set first game in week equal to iterator
            dbPathWeek = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/games'
            week = root.child(dbPathWeek).get() #get the games for this week from database
            gamesInWeek = len(week) #get the number of the games in this week
            lastGameInWeek = firstGameInWeek + gamesInWeek #calculate the iterator for the last game in the week
            for j in range (0, gamesInWeek): #iterate through games in week in database
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
                homeBoth = homeCity + ' ' + homeName #save the home team city and name i.e. New England Patriots
                awayCity = root.child(dbPathAwayCity).get()
                awayName = root.child(dbPathAwayName).get()
                awayBoth = awayCity + ' ' + awayName #save the away team city and name
                for k in range(firstGameInWeek, lastGameInWeek): #for each pick in the week, check if it was for this game
                    userName = userNames[user]
                    userPick = obj.root.row[k][userName]
                    if userPick == "St. Louis" or userPick == "St. Louis Rams": #deal with using St. Louis as an abbreviation for Saint Louis
                        userPick = "Saint Louis Rams"
                    elif userPick == "Rams": #deal with Rams changing cities
                        if obj.root.row[i]['Season'] == '2015-2016' or obj.root.row[i]['Season'] == '2014-2015':
                            userPick = "Saint Louis Rams"
                        else:
                            userPick = "Los Angeles Rams"
                    elif userPick == "Chargers": #deal with Chargers changing cities
                        if obj.root.row[i]['Season'] == '2017-2018':
                            userPick = "Los Angeles Chargers"
                        else:
                            userPick = "San Diego Chargers"
                    if userPick in homeBoth or userPick in awayBoth: #if the user pick is for this game
                        dbSetUserPickPath = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/' + str(gameId)
                        if userPick == homeBoth or userPick == awayBoth: #if the user pick is already the full name
                            newPick = root.child(dbSetUserPickPath).set({ #record pick in the database
                                'pick' : userPick
                            })
                        else: #if the user only had city or name
                            userPick = teams[userPick] #get the full name from dictionary
                            newPick = root.child(dbSetUserPickPath).set({ #record pick in database
                                'pick' : userPick
                            })
                        print gameId, userPick
                        if userPick == homeBoth: #if the user picked the home team
                            dbPathHome = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/games/' + str(gameId) + '/home/winner'
                            correct = root.child(dbPathHome).get() #get whether home team won
                            if correct: #if the home team won
                                weekCorrectCount += 1 #add one to the number of correct picks for this week
                            else: #if the home team did not win
                                weekIncorrectCount += 1 #add one to the number of incorrect picks for this week
                        elif userPick == awayBoth: #if the user picked the away team
                            dbPathAway = obj.root.row[i]['Season'] + '/weeks/week' + str(obj.root.row[i]['Week']) + '/games/' + str(gameId) + '/away/winner'
                            correct = root.child(dbPathAway).get() #get whether away team won
                            if correct: #if the away team won
                                weekCorrectCount += 1 #add one to the number of correct picks for this week
                            else: #if the away team did not win
                                weekIncorrectCount += 1 #add one to the number of incorrect picks for this week
            dbPathUserWeek = 'users/' + UIDs[user] + '/seasons/' + obj.root.row[i]['Season'] + '/weeks/' + weekId
            newCorrect = root.child(dbPathUserWeek).update({ #when all games in the week have been gone through
                'correct' : weekCorrectCount #update number of correct picks for this week in the database
            })
            newIncorrecrt = root.child(dbPathUserWeek).update({
                'incorrect' : weekIncorrectCount #update number of incorrect picks for this week in the database
            })
            seasonCorrect += weekCorrectCount #add the number of correct picks for the week to the number of correct picks for the season
            seasonIncorrect += weekIncorrectCount #add the number of incorrect picks for the week to the number of incorrect picks for the season
            weekCorrectCount = 0 #reset the number of correct and incorrect picks for the week
            weekIncorrectCount = 0
    totalCorrect += seasonCorrect #when the user ends, update the total number of correct and incorrect picks from the last season for the user
    totalIncorrect += seasonIncorrect
    dbUserPath = 'users/' + UIDs[user]
    dbLastSeasonPath = 'users/' + UIDs[user] + '/seasons/' + seasonId
    root.child(dbLastSeasonPath).update({ #update database to hold number of correct and incorrect picks for the last season
        'correct' : seasonCorrect,
        'incorrect' : seasonIncorrect
    })
    root.child(dbUserPath).update({ #update the total number of correct and incorrect picks for the user in the database
        'correct' : totalCorrect,
        'incorrect' : totalIncorrect
    })