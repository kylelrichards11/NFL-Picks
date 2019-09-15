import untangle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

obj = untangle.parse('currenWeek.xml') #make an object from the XML

season = '2018-2019'
week = 'week3'