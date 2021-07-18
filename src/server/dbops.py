# this file contains methods necessary for DB operations
import sys
sys.path.append('./../')

from datetime import datetime
from server_config import DATABASE_NAME,COLLECTION_NAME,MODE
from puzzler import puzzle_gen

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

def compose(username,contested_password,index_number):
    '''
        this function composes the complex hash stored as  a database
    '''
    from hasher import getNumber
    contested_id = getNumber(username,contested_password)%index_number
    from pymongo import MongoClient
    db_location = MongoClient('mongodb://localhost:27017')
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]

    data_from_db = db_collection.find_one({'index':contested_id})

    try:
        from hasher import hashify
        return hashify(contested_password,data_from_db)
    except:
        print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Index Number doesnot match any entry')
        if MODE == 'DEBUG':
            print(f'DATA => username ::  {username}, password :: {contested_password}, index_number :: {index_number}')
        return 'invalid'
    
def verify(username,password):
    '''
        this function verifies the username and password
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]

    # get all the data from the database
    data_from_db = db_collection.find()

    # iterate over all the data in the database
    # O(n) is too complex, reduce using indexes 
    for i in data_from_db:
        # check if the username and password matches
        if i['username'] == username and compose(password,i['index']) == i['password'] and i['password']!='invalid':
            return True
    return False
