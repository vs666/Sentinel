from flask import *
from server_config import PORT,DEFAULT_TARGET_URL,DEFAULT_FALLBACK_URL
from dbops import appendData
# creating a flask app
app = Flask(__name__)

@app.route('/authenticate')
def authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
    portal = request.args.get('portal')
    '''
        explore the option of receiveing hashed password
    '''

    # make use of portal option for allowing specific authentication services or 
    # to decide the destination url for successful authentication
    

@app.route('/signUp')
def signUp():
    username = request.args.get('username')
    password = request.args.get('password')
    portal = request.args.get('portal')
    
    # for now we keep the same fallback and target and stuff
    '''
        Complicate the password here 
    '''

    # we also allocate index value here 
    index = 0
    # Now we hope the password has been complicated.
    ddict = {
        "username":username,
        "password":password,
        "portal":'DEFAULT',
        "target_url":DEFAULT_TARGET_URL,
        "fallback_url":DEFAULT_FALLBACK_URL,
        "index":index
    }

    if appendData(ddict):
        # data append succesful
        return 'Succesful'
    else:
        # data append failed
        return 'Failed'
        

if __name__ == '__main__':
    # run the app
    app.run(debug=True,port=PORT)
