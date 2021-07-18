from flask import *
from puzzler import puzzle_gen
from config import PORT
# creating a flask app
app = Flask(__name__)

@app.route('/solve_puzzle',methods=['GET','POST'])
def solve_puzzle():
    # print('hello world')
    # return request.get_json()
    # # print(request.view_args)
    username = request.get_json()['username']
    password = request.get_json()['password']
    mad = request.get_json()['mac_address']
    '''
        check mac-address here
    '''
    num = puzzle_gen(username,password)
    return {"number":num}

if __name__ == '__main__':
    # run the app
    app.run(debug=True,port=PORT)



# with app.test_client() as c:
#     rv = c.post('/solve_puzzle',json={
#         'username':'dodo.zozo','password':'kronos','mac_address':'maddy'})
#     json_data = rv.get_json()
#     print(json_data)
