# this file contains methods necessary for DB operations
from datetime import datetime
from server_config import DATABASE_NAME,COLLECTION_NAME,MODE

def verifyDictionary(d):
    from server_config import sample_dict
    assert(type(d) ==  type(sample_dict))

    expectedKeys = sample_dict.keys()
    for i in d.keys():
        if i not in expectedKeys:
            return False
    if len(d.keys()) != len(sample_dict.keys()):
        return False
    return True


def appendData(data_dictionary):
    ''' 
        this function appends the data to mongodb database
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")

    # creates database if not exists, if exists instantiates lhs with it's object
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]


    if verifyDictionary(data_dictionary):
        # verified 
        try:
            db_collection.insert_one(data_dictionary)
            return True
        except:
            # log to the log of errors ( change from stdout to logfile later )
            print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Exception occoured while appending data to database')
            return False
    else:
        print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Dictionary requested to be appended is of invalid format')
        if MODE == 'DEBUG':
            print('DATA => ',data_dictionary)
        return False



