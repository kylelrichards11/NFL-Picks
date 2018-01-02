import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('NFL-Picks-11f89026ddbd.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://nfl-picks-b5e4d.firebaseio.com'
})
root = db.reference()

teams = { 
    "Arizona Cardinals" : "ARI",
    "Atlanta Falcons" : "ATL",
    "Baltimore Ravens" : "BAL",
    "Buffalo Bills" : "BUF",
    "Carolina Panthers" : "CAR",
    "Chicago Bears" : "CHI",
    "Cincinnati Bengals" : "CIN",
    "Cleveland Browns" : "CLE",
    "Dallas Cowboys" : "DAL",
    "Denver Broncos" : "DEN",
    "Detroit Lions" : "DET",
    "Green Bay Packers" : "GB",
    "Houston Texans" : "HOU",
    "Indianapolis Colts" : "IND",
    "Jacksonville Jaguars" : "JAX", #FOR 2015 CHANGE JAX TO JAC
    "Kansas City Chiefs" : "KC",
    "Los Angeles Rams" : "LA",
    "Los Angeles Chargers" : "LAC",
    "Miami Dolphins" : "MIA",
    "Minnesota Vikings" : "MIN",
    "New England Patriots" : "NE",
    "New York Giants" : "NYG",
    "New York Jets" : "NYJ",
    "New Orleans Saints" : "NO",
    "Oakland Raiders" : "OAK",
    "Philadelphia Eagles" : "PHI",
    "Pittsburgh Steelers" : "PIT",
    "San Diego Chargers" : "SD",
    "Seattle Seahawks" : "SEA",
    "San Francisco 49ers" : "SF",
    "Saint Louis Rams" : "STL",
    "Tampa Bay Buccaneers" : "TB",
    "Tennessee Titans" : "TEN",
    "Washington Redskins" : "WAS"
}

obj = untangle.parse('2017Data.xml') #CHANGE FILE NAME FOR EACH YEAR
max = len(obj.root)
for i in range(0, max):
    teamName = obj.root.row[i]['Team']
    teamId = teams[teamName]
    dbPath = '2017-2018/teams/' + teamId #CHANGE PATH FOR EACH SEASON
    root.child(dbPath).update({
        'teamId' : teamId,
        'city' : obj.root.row[i]['City'],
        'name' : obj.root.row[i]['Name'],
        'currentWins' : obj.root.row[i]['W'],
        'currentLosses' : obj.root.row[i]['L'],
        'currentTies' : obj.root.row[i]['T'],
        'pointsFor' : obj.root.row[i]['PF'],
        'pointsAgainst' : obj.root.row[i]['PA']
    })