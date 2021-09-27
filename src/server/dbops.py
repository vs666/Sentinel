# this file contains methods necessary for DB operations
import sys

from hasher import getNumber,hashify
sys.path.append('./../')
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime
from server_config import DATABASE_NAME,COLLECTION_NAME,MODE,NF_URL,SIGN_COLLECTION
from nacl.signing import VerifyKey

def verifyDictionary(d):
    from server_config import sample_dict
    assert(type(d) ==  type(sample_dict))
    return True
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
    contested_id = getNumber(username,contested_password)
    from pymongo import MongoClient
    db_location = MongoClient('mongodb://localhost:27017')
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]
    index_number+=1
    data_from_db = db_collection.find_one({'index':contested_id%index_number})

    try:
        from hasher import hashify
        return hashify(contested_password,data_from_db['username'],contested_id)
    except:
        print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Index Number doesnot match any entry')
        if MODE == 'DEBUG':
            print(f'DATA => username ::  {username}, password :: {contested_password}, index_number :: {index_number}')
        return 'invalid'

def verify(username,password,portal):
    '''
        this function verifies the username and password
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]

    # get all the data from the database
    data_from_db = db_collection.find_one({'username':username,'portal':portal})
    if data_from_db == None:
        return NF_URL
    if data_from_db['username'] == username and compose(username,password,data_from_db['index']) == data_from_db['password'] and data_from_db['password']!='invalid':
        return data_from_db['target_url']
    else:
        return data_from_db['fallback_url']





def checkSignature(portal,username,password,signature):
    '''
        this function verifies the signature
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]
    data_from_db = db_collection.find_one({'portal':portal})
    pub_k = data_from_db['public_key'] 
    from nacl.signing import VerifyKey
    verf_k = VerifyKey(pub_k)
    try:
        verf_k.verify(username+password,signature)
        return True
    except:
        return False
    
def hashify_pass(username,password):
    '''
        this function creates hash of the password
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[COLLECTION_NAME]

    num = getNumber(username, password)
    if db_collection.find_one({'username':username})!= None:
        print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Entry already exists')
        return None,-1

    # get all the data from the database
    data_from_db = db_collection.count()
    index = data_from_db
    mapped_id = db_collection.find_one({"index":(num%index)})
    print('mapped ID is :: ',mapped_id)
    return hashify(password,mapped_id['username'],num),index


def check_signature(portal,sign,content):
    '''
        Verify the signature against public key provided in the db 
        Before that make sure the portal is valid (present in the database
    '''
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[SIGN_COLLECTION]
    data_from_db = db_collection.find_one({'portal':portal})
    if data_from_db == None:
        return False
    pub_key = data_from_db['public_key']
   
    '''
            ---COPILOT GENERATED CODE, CHECK ONCE---
    '''
    verf_k = VerifyKey(pub_key)
    try:
        verf_k.verify(content,sign)
        return True
    except:
        return False
        

def addClient(data:dict):
    '''
        load data into signed collection pymongo
    '''    
    from pymongo import MongoClient
    db_location = MongoClient("mongodb://localhost:27017/")
    db_object = db_location[DATABASE_NAME]
    db_collection = db_object[SIGN_COLLECTION]
    if db_collection.find_one({'portal':data['portal']}) != None:
        print('LOG:: [',datetime.now().strftime("%d-%m-%Y||%H:%M:%S"),'] => Entry already exists')
        return False,'Entry already exists'
    else:
        try:
            db_collection.insert_one(data)
            return True,'Success'
        except:
            return False,'Database fault'
