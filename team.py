import db
import pymongo
from pprint import pprint

class Team:

    def __init__(self, tid):

        orList = [ {"teamID":i} for i in tid.split("-") ]
        self.conn = db.connect()
        # look for the team by the id passed and sort on the year in descending order
        self.docs = list(self.conn.teams.find(
                { '$or': orList }, 
                {   '_id': False    } 
            ).sort(   'yearID',   pymongo.DESCENDING  ) )
        self.name = self.docs[0]['name']

    def __repr__(self):
        return "<Team: {}>".format(self.name) 