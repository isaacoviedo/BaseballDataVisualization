import pymongo
import os
import pandas as pd
import sys

# connects to the baseball db
def connect():

    client = pymongo.MongoClient("mongodb://localhost:27017")

    return client['baseballdb']

# creates all collections in the database
def colls_create():

    PATH = ".\\baseballdatabank-2019.2\\core\\"
    conn = connect()
    colls = conn.list_collection_names()

    for filename in os.listdir(PATH):
        
        collname, _ = filename.split('.')
        collname = collname.lower()

        # don't want to have to import a collection twice
        if filename.endswith(".csv") and (collname not in colls):
            print("Importing: {}".format(filename))
            cmd = "mongoimport -d baseballdb -c {} --type csv --file {}{} --headerline".format(collname,PATH,filename)
            os.system(cmd)
    
    return

if __name__ == "__main__":
    colls_create()