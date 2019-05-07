from db import connect
from pprint import pprint

def get_active_teams():
    '''
        - @returns: list of documents for active franchises with the following format
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