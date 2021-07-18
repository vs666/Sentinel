PORT = 5000

COLLECTION_NAME = 'authentication-collection'
DATABASE_NAME = 'authentication-database'

# this is sample of the dictionary that can be inserted in the database 
sample_dict = {
    "username":"lorem",
    "password":"ipsum",
    "index":0,
    "target_url":"go-to this url on authentication",
    "fallback_url":"go-to this url on failing to authenticate"
}

MODE = 'DEBUG'

# random urls don't judge
DEFAULT_TARGET_URL = 'https://www.google.com'
DEFAULT_FALLBACK_URL = 'https://www.iiit.ac.in'
LOCKED_URL = '127.0.0.1:9000'
