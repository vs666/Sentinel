import hashlib
import requests
import uuid
from server_config import LOCKED_URL

def hashify(password,mapped_email):
    thorax = hashlib.sha256(bytes(password+mapped_email,encoding='utf-8')).hexdigest()
    return thorax

def getNumber(username,password):
    r = requests.get(url=LOCKED_URL+'/solve_puzzle',params={"mac_address":uuid.getnode(),"username":username,"password":password})
    data = r.json()
    return data['number']
