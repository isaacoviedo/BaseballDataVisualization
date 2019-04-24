import pymongo
import os
import pandas as pd
import sys

# connects to the baseball db
def connect():

    url = os.environ.get("MONGO_SERVER")
    client = pymongo.MongoClient(url)

    return client['baseballdb']

# creates all collections in the database
def colls_create():

    PATH = ".\\baseballdatabank-2019.2\\core\\"
    conn = connect()
    colls = conn.list_collection_names()

    USER = os.environ.get("MONGO_SERVER_USER")
    PASS = os.environ.get("MONGO_SERVER_PASS")

    for filename in os.listdir(PATH):
        
        collname, _ = filename.split('.')
        collname = collname.lower()

        # don't want to have to import a collection twice
        if filename.endswith(".csv") and (collname not in colls):
            print("Importing: {}".format(filename))
            
            if "atlas" in sys.argv:
                cmd = 'mongoimport --host baseballdb-shard-0/baseballdb-shard-00-00-d4jyf.mongodb.net:27017,baseballdb-shard-00-01-d4jyf.mongodb.net:27017,baseballdb-shard-00-02-d4jyf.mongodb.net:27017 --ssl --username {} --password {} --authenticationDatabase admin --db baseballdb --collection {} --type csv --file {}{} --headerline'.format(USER,PASS,collname,PATH,filename)
            else:
                cmd = "mongoimport -d baseballdb -c {} --type csv --file {}{} --headerline".format(collname,PATH,filename)
            os.system(cmd)
    
    return

if __name__ == "__main__":
    colls_create()