PORT = 5000

MAX_PASS_LENGTH = 50
MAX_USERNAME_LENGTH = 80

DATABASE_NAME = 'authentication-database'
COLLECTION_NAME = 'authentication-collection'
SIGN_COLLECTION = 'sign-collection'



# this is sample of the dictionary that can be inserted in the database 
sample_dict = {
    "username":"lorem",
    "password":"ipsum",
    "index":0,
    "target_url":"go-to this url on authentication",
    "portal":'...',
    "fallback_url":"go-to this url on failing to authenticate"
}

MODE = 'DEBUG'
PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
BLAH...
BLAH...
-----END PUBLIC KEY-----'''


# random urls don't judge
DEFAULT_TARGET_URL = 'https://www.google.com'
DEFAULT_FALLBACK_URL = 'https://www.iiit.ac.in'
LOCKED_URL = 'http://127.0.0.1:'
NF_URL = 'https://www.notfound.co.in'

# max ports subnet is running on 
MAX_PORT_COUNT = 5 # should be 10 ?? 
