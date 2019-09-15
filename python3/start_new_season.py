import json
from urllib.request import urlopen
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

def init_firebase():
    cred = credentials.Certificate("config.json")
    fb = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://nfl-picks-b5e4d.firebaseio.com'
    })

