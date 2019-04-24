import db
import pymongo
from pprint import pprint

class Player:

    def __init__(self, pname):
        
        self.conn = db.connect()
        self.pname = pname
        fname, lname = pname.split()
        self.people = db.connect().people.find_one(
            {"$or": [
                        {"nameGiven": {"$regex": pname}},
                        {"$and":
                            [
                                {"nameFirst": {"$regex": fname}},
                                {"nameLast": {"$regex": lname}}
                            ]
                        }
                    ]
            }
        )

    def __repr__(self):
        return "<Player: {} {}>".format(self.fname,self.lname)
    
    def get_appearances(self):

        # Appearances are by year
        self.appearances = self.conn.appearances.find( { "playerID": self.people['playerID'] }).sort("yearID", pymongo.DESCENDING)

        for elem in self.appearances:
            print(elem)

        return self.appearances
