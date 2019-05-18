from db import connect
from player import Player
from pprint import pprint

def get_active_teams():
    '''
        :returns: list of documents for active franchises with the following format
            - franchName : name of the franchise
            - franchID : id of the franchise  
    '''

    conn = connect()

    query = {
        'active':'Y',
    }

    project = {
        '_id':0,
        'franchID':1,
        'franchName':1
    }

    results = conn.teamsfranchises.find(query,project)
    return list(results)

def get_search_results(player_name):
    '''
        :param player_name: name of the player given in the search bar as input
        :returns : list of players that could be who they are searching for 
    '''

    conn = connect()
    cursor = conn.people

    # we want the name in the db to have all of the input given by the user
    name_regex = '&'.join(player_name.split()) # NOTE : THIS IS THE REGULAR EXPRESSION FOR THE NAME
    split_name = player_name.split()
    len_split_name = len(split_name)
    
    andList = []
    orList = []
    query = {}

    # Handle the case when the user gives one word, two words, or three or more words as the input
    if len_split_name  == 1:
        fName = split_name[0]
        orList.append({'nameFirst': { '$regex' : fName , '$options': 'i'} })
        orList.append({'nameLast' : {'$regex': fName, '$options' : 'i'} })

    elif len_split_name == 2:
        fName, lName = split_name[0], split_name[1]
        andList.append( {'nameFirst': { '$regex': fName, '$options':'i' }} )
        andList.append( {'nameLast':  { '$regex': lName, '$options':'i' }} )
        
    elif len_split_name > 2:
        fName, lName = split_name[0], split_name[-1]
        andList.append( {'nameFirst': { '$regex': fName, '$options':'i' }} )
        andList.append( {'nameLast':  { '$regex': lName, '$options':'i' }} )

    # Following query in SQL:
    #
    #   SELECT  * 
    #   FROM    PEOPLE
    #   WHERE   ( nameFirst = fName AND nameLast = lName ) OR ( nameGiven LIKE 'N_1|N_2|...|N_i' ) 
    #

    query = { '$and' : andList } if len_split_name >= 2 else { '$or' : orList }

    projection = {
        '_id' : 0
    }

    # results = list(cursor.find(query, projection))

    # Testing out how long it takes to return a list of players
    results = [ Player( p['playerID'] ) for p in cursor.find(query,projection) ]

    return results