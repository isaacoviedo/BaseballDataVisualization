import db
import pymongo
from pprint import pprint

class Player:

    def __init__(self, playerID):
        self.conn = db.connect()
        self.profile = self.conn.people.find_one( {'playerID':playerID}, {'_id':0} )
        self.fName, self.lName = self.profile['nameFirst'], self.profile['nameLast']
        self.playerID = playerID

    def __repr__(self):
        return "<Player: {} {}>".format(self.fName,self.lName)
    
    def get_appearances(self):

        # Appearances are by year
        self.appearances = self.conn.appearances.find( { "playerID": self.people['playerID'] }).sort("yearID", pymongo.DESCENDING)

        for elem in self.appearances:
            print(elem)

        return self.appearances

    def get_teams(self):
        '''
            :returns: all the teams the player has played for
        '''

        # first find all the teamids that the player has appearances with
        query = {
            'playerID' : self.playerID
        }
        projection = {
            '_id':0,
            'teamID':1
        }
        results = list(self.conn.appearances.find(query,projection).distinct('teamID'))

        # next find the franchise id of the teams they have appearances for
        franchQuery = { '$or' : [ {'teamID': teamID} for teamID in results  ] }
        franchProj = { '_id':0, 'franchID':1 }
        franch_results = list(self.conn.teams.find(franchQuery, franchProj).distinct('franchID'))

        return franch_results

    def get_team_name(self):
        '''
            :returns: the name of the team the player last played for.
        '''

        match_stage = {
            'playerID': self.playerID
        }

        group_stage = {
            '_id': '$teamID', 
            'yearLastPlayed': {
                '$max': '$yearID'
            }
        }

        sort_stage = {
            'yearLastPlayed': -1
        }

        limit_stage = 1

        pipeline = [
            {
                '$match': match_stage
            }, {
                '$group': group_stage
            }, {
                '$sort': sort_stage
            }, {
                '$limit': limit_stage
            }
        ]

        result = self.conn.appearances.aggregate(pipeline).next()
        # Of the form: { '_id' : teamID, 'yearLastPlayed': yearID }

        query = {
            'teamID': result['_id']
        }

        projection = {
            '_id':0,
            'name':1
        }

        result = self.conn.teams.find(query,projection).sort('yearID',pymongo.DESCENDING).next()
        
        return result['name']

    def get_salaries(self):
        '''
            :returns: two lists one for the years and another for the salaries
        '''

        cursor = self.conn.salaries

        match_stage = {
            'playerID': self.playerID
        }

        group_stage = {
            '_id' : '$playerID',
            'yearList' : { '$push' : '$yearID' },
            'salaryList' : { '$push' : '$salary' }
        }

        pipeline = [
            {
                '$match': match_stage
            }, {
                '$group': group_stage
            }
        ]

        try:
            results = cursor.aggregate(pipeline).next()
            return results['salaryList'], results['yearList']
        except StopIteration:
            return [], []