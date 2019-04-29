import db
import pymongo
from pprint import pprint

class Team:

    def __init__(self, tid):

        self.tidOrList = [ {"teamID":i} for i in tid.split("-") ]

        self.conn = db.connect()
        self.docs = list(self.conn.teams.find(
                { '$or': self.tidOrList }, 
                {   '_id': False    } 
            ).sort(   'yearID',   pymongo.DESCENDING  ) )
        self.name = self.docs[0]['name']

    def __repr__(self):
        return "<Team: {}>".format(self.name)


    def gen_minmax(self, fieldList):
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

        for elem in fieldList:
            fldName = '${}'.format(elem)
            
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
                    '$or': self.tidOrList
                }
            }, {
                '$group': group_stage
        }]

        return list(self.conn.teams.aggregate(pipeline))[0]