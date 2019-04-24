import db
import pymongo
from pprint import pprint

class Team:

    def __init__(self, tname):
        self.conn = db.connect()
        self.docs = list(self.conn.teams.find({
            'name': {'$regex':tname, '$options':'i'}
        }, {'_id': False}).sort('yearID',pymongo.DESCENDING))
        self.name = tname

    def __repr__(self):
        return "<Team: {}>".format(self.name) 