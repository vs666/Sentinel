from hashlib import sha256
from typing import Protocol
from flask import *
import flask
from server_config import PORT,DEFAULT_TARGET_URL,DEFAULT_FALLBACK_URL,MAX_PASS_LENGTH,MAX_USERNAME_LENGTH,PUBLIC_KEY
from dbops import checkSignature, hashify_pass,verify,addClient,check_signature
from flask_cors import CORS
# creating a flask app


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/authenticate',methods=['GET','POST'])
def authenticate():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        portal = request.get_json()['portal'] or None
        if len(password) > MAX_PASS_LENGTH:
            return {'status':'Failed','log':'Password Length too big'}
        elif len(username) > MAX_USERNAME_LENGTH:
            return {'status':'Failed','log':'Username Length too big'}
        
        '''
            explore the option of receiveing hashed password
        '''
        # RUN Verification with portal stuff ????
        destUrl = verify(username,password,portal or 'DEFAULT')
        return redirect(destUrl)
    except:
        return {'status':'Failed','log':'Unhandled server exception'}

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    
    # handle errors (no portals etc.) so that client request can't crash the server
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        portal = request.get_json()['portal'] or 'DEFAULT'  # compulsory for a login based service
        if len(password) > 50:
            return {'status':'Failed','log':'Password Length too big'}
        elif len(username) > 80:
            return {'status':'Failed','log':'Username Length too big'}
        elif len(portal) > 80:
            return {'status':'Failed','log':'Portal Length too big'}
    except:
        return {'status':'error','log':'server unable to handle request'}
    # for now we keep the same fallback and target and stuff
    
    ''' 
        Authentication of portal against Database before sending the request to the target
    '''
    try:
        if portal != 'DEFAULT':
            content = request.get_json()['content']
            signature = request.get_json()['signature']
            if sha256(str(username+password+portal).encode('utf-8')).hexdigest() != content or check_signature(portal,signature,content)==False:
                return {'status':'error','log':'invalid portal or unidentified signature'}
    except:
        return {'status':'error','log':'server rejected malicious or incomplete request'}
    

    # we also allocate index value here 
    # Now we hope the password has been complicated.
    ddict = {
        "username":username,
        "password":password,
        "portal":(portal or 'DEFAULT'),
        "target_url":DEFAULT_TARGET_URL,
        "fallback_url":DEFAULT_FALLBACK_URL,
        "index":-1
    }
    
    try:
        ddict['target_url'] = request.get_json()['target_url']
    except:
        ddict['target_url'] = DEFAULT_TARGET_URL
    try:
        ddict['fallback_url'] = request.get_json()['fallback_url']
    except:
        ddict['fallback_url'] = DEFAULT_FALLBACK_URL
    try:
        #  check the signature here only
        proposed_signature = request.get_json()['signature']
        from dbops import checkSignature
        if not checkSignature(portal,username,password,proposed_signature):
            return {'status':'failure','reason':'Signature is not valid'}
    except:
        pass
    ph,ind = hashify_pass(username,password)
    if ind == -1:
        return {'status':'Failed','log':'Username already exists'}
    ddict['password'] = ph
    ddict['index'] = ind
    from dbops import appendData
    if appendData(ddict):
        # data append succesful
        return {'status':'Success','username':ph}
    else:
        # data append failed
        return {'status':'Failed'}




'''
    Add authentication service
    accepts 
'''
@app.route('/registerBusiness',methods=['GET','POST'])
def registerBusiness():
    try:
        business_name = request.get_json()['business_name']
        portal = request.get_json()['portal']
        public_key = request.get_json()['public_key']
        redirection_url = request.get_json()['redirection_url'] or 'None'
        # # resolve this later
        # redirection_url = request.get_json()['redirection_url'] # url to send response to (usually the same as the caller tho) 

        data = {
            'business_name':business_name,
            'portal':portal,
            'public_key':public_key,    # HEX DIGEST OF THE PUBLIC KEY
            'redirection_url':redirection_url,
        }
        cond,msg = addClient(data)
        if cond:
            return {'status':'Success','log':'Client registered'}
        else:
            return {'status':'Failed','log':msg}    # check if this can be used to access info about the database (?)
    except:
        return {'status':'Failed','log':'Unable to parse request'}



'''
    Make a function to give public key for verification of digital signature to anyone who asks
'''
@app.route('/getPublicKey',methods=['GET','POST'])
def getPK():
    return {'public_key': PUBLIC_KEY}



@app.route('/knock')
def knock():
    return '''
        <h1> Hey, I am a messenger from the server</h1>
        <p> Don't worry, I am up and running</p>
    '''        

if __name__ == '__main__':
    # run the app
    app.run(debug=True,port=PORT)
