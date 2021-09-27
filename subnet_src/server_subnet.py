from logging import debug
from flask import *
from puzzler import puzzle_gen
from config import PORT
import sys
import multiprocessing
# creating a flask app
app = Flask(__name__)

@app.route('/solve_puzzle',methods=['GET','POST'])
def solve_puzzle():
    # print('hello world')
    # return request.get_json()
    # print(request.get_data())
    username = request.get_json()['username']
    password = request.get_json()['password']
    print('USERNAME => ',username,'PASSWORD => ',password)
    mad = request.get_json()['mac_address']
    '''
        check mac-address here
    '''
    num = puzzle_gen(username,password)
    print("NUMBER IS : ",num)
    return {"number":num}

@app.route('/ping')
def ping():
    return 'Server subnet is up'

def start_server(_PORT):
    debug('starting server')
    app.run(port=_PORT,debug=True)

if __name__ == '__main__':
    # run the app
    processes = []
    # number of ports
    nPorts = int(sys.argv[2])
    nPorts = min(nPorts,10) # max 10 to spare my innocent PC :P 
    for i in range(nPorts):
        p = multiprocessing.Process(target=start_server,args=[PORT+i])
        p.start()
        processes.append(p) 

    # PORT = int(sys.argv[1]) 
    # app.run(debug=True,port=PORT)


