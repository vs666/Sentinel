import hashlib
import requests
import uuid
from server_config import LOCKED_URL,MAX_PORT_COUNT
import random
def hashify(password,mapped_email,num):
    thorax = hashlib.sha256(bytes(password+mapped_email+str(num),encoding='utf-8')).hexdigest()
    return thorax

def getNumber(username,password):
    port = random.randint(0,MAX_PORT_COUNT)
    r = requests.get(url=LOCKED_URL+str(9000+port)+'/solve_puzzle',json={"mac_address":uuid.getnode(),"username":username,"password":password})
    print('KACHING',r)
    data = r.json()
    return data['number']
