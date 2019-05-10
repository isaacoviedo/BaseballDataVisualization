import db
import pymongo
from pprint import pprint

class Team:

    def __init__(self, franchid = ""):

        self.conn = db.connect()

        if franchid:
            self.franchid = franchid
            self.docs = list(self.conn.teams.find(
                    { 'franchID': self.franchid }, 
                    {   '_id': False    }
                ).sort(   'yearID',   pymongo.DESCENDING  ) )
            self.name = self.docs[0]['name']

    def __repr__(self):
        return "<Team: {}>".format(self.name)

    def get_all_names(self):
        '''
            purpose:
                - used to find all the names the team has had throughout the years
            param:
                - none
            returns:
                - list of documents with the following format
                    - "_id" : name of the team
                    - "year_end" : when the team stopped going by the name ("_id")
                    - "year_start" : when the team started going by the name
        '''

        match_stage = {
            'franchID': self.franchid
        }

        group_stage = {
            '_id' : '$name',
            'year_start' : { '$min':'$yearID' },
            'year_end': { '$max':'$yearID' }
        }

        sort_stage = {
            'year_end' : -1
        }

        pipeline = [
            {
                '$match': match_stage
            }, {
                '$group': group_stage
            }, {
                '$sort': sort_stage
            }
        ]

        return list(self.conn.teams.aggregate(pipeline))

    def find_by_teamID(self, teamID):

        res = self.conn.find_one({'teamID' : teamID})

        return res.next() if len(list(res)) != 0 else {}

    def gen_minmax(self, fieldList = ['yearID','Rank','W','L','2B','3B','HR','SB','ERA','HRA']):
        '''
            purpose: 
                - used for finding the min/max of each label in the parallel coordinate plot
            param: gen_minmax( self, fieldList )
                - fieldList-{list} of all the fields that we want to find the min and max for
            returns:
                - dict with min/max values of given fieldList 
        '''

        # want to create the group stage for a custom number of fields
        group_stage = { '_id': '' }

        project_stage = {   '_id': 0,
                            'SB': { '$cond': [ { '$eq': ["$SB", ""] }, 0, "$SB" ] },
                        }

        for elem in fieldList:
            fldName = '${}'.format(elem)
            
            if elem == 'SB':
                pass
            else:
                project_stage[elem] = 1

            # ---- min of the field
            minKey = 'min_{}'.format(elem)
            minVal = { '$min' : fldName }
            # ---- max of the field
            maxKey = 'max_{}'.format(elem)
            maxVal = { '$max' : fldName }

            group_stage[minKey] = minVal
            group_stage[maxKey] = maxVal

        pipeline = [
            {
                '$match': {
                    'franchID': self.franchid
                }
            }, {
                '$project': project_stage
            }, {
                '$group': group_stage
        }]

        return list(self.conn.teams.aggregate(pipeline))[0]