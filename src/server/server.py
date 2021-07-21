from flask import *
from server_config import PORT,DEFAULT_TARGET_URL,DEFAULT_FALLBACK_URL
from dbops import checkSignature, hashify_pass,verify
# creating a flask app
app = Flask(__name__)

@app.route('/authenticate',methods=['GET','POST'])
def authenticate():
    username = request.get_json()['username']
    password = request.get_json()['password']
    portal = request.get_json()['portal']
    '''
        explore the option of receiveing hashed password
    '''
    print('Request for authentication : ',username,password)

    destUrl = verify(username,password)
    return redirect(destUrl)


@app.route('/signUp',methods=['GET','POST'])
def signUp():
    username = request.get_json()['username']
    password = request.get_json()['password']
    portal = request.get_json()['portal']
<<<<<<< HEAD
=======

>>>>>>> 45861bd5ede17659b1fc66c3de7972c90ba2e19d
    # for now we keep the same fallback and target and stuff
    '''
        Complicate the password here
    '''
    # we also allocate index value here
    # Now we hope the password has been complicated.
    ddict = {
        "username":username,
        "password":password,
        "portal":'DEFAULT',
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


@app.route('/knock')
def knock():
    return '''
        <h1> Hey, I am a messenger from the server</h1>
        <p> Don't worry, I am up and running</p>
    '''

if __name__ == '__main__':
    # run the app
    app.run(debug=True,port=PORT)
