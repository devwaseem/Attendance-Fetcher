from flask import Flask,request
import json

from config import PORT
from services import checklogin,fetchAttendance
import error_codes as ERROR

app = Flask(__name__)
app.debug = True

@app.route('/')
def mainEndPoint():
   return json.dumps({
       "status":True,
       "Message":"Welcome to TCS-ion Fetcher Webservice"
   })

@app.route('/login',methods =["POST"])
def login():
    username = str(request.json["username"]).strip()
    password = str(request.json["password"]).strip()
    if username and password:
        if checklogin(username,password):
            return json.dumps({
                "status": True,
                "Message": "Login Successful"
            })
        else:
            return json.dumps({
                "status": False,
                "code":ERROR.CREDENTIALS,
                "Message": "Credentials Incorrect"
            })
    else:
        return json.dumps({
            "status": False,
            "code": ERROR.MISSING_FIELDS,
            "Message": "Please fill all the Fields"
        })


@app.route('/fetch',methods =["POST"])
def fetch():
    username = str(request.json["username"]).strip()
    password = str(request.json["password"]).strip()
    if username and password:
        return fetchAttendance(username,password)
    else:
        return json.dumps({
            "status": False,
            "code": ERROR.MISSING_FIELDS,
            "Message": "Please fill all the Fields"
        })





if __name__ == '__main__':
   app.run(host = '0.0.0.0',port=PORT)
