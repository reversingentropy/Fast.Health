from flask import Flask, render_template
from datetime import datetime
from model.User import User
from validation.Validator import *
#from model.Iris_predict import Iris_SVC, Iris_DB
import bcrypt
import pickle
import numpy as np

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Login
@app.route('/login', methods=['POST'])
def verifyUser():
    try:
        email = request.form['email']
        password = request.form['pwd']
        print(email, password)
        ret = User.loginUser(email, password)
        token = ret['jwt']
        userid = ret['userid']
        username = ret['username']
        if len(token) > 0:
            results = Iris_DB.getAllPrediction(userid)
            resp = make_response(render_template('mainPage.html', username= username, results=results, prediction=""))
            resp.set_cookie('jwt', token)
            return resp, 200
        else:
            resp = make_response(render_template('login.html',  message='Invalid Login Credentials!'))
            resp.set_cookie('jwt', '')
            return resp, 404
    except Exception as err:
        print(err) #for debugging 
        message = 'Invalid Login Credentials!'
        resp = make_response(render_template('login.html',  message=message))
        return resp, 404

@app.route('/')
def home():
	return render_template('index.html')
#	return render_template('home.html')
	
@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/user')
def user():
    print('user page')
    return render_template('users.html')
	
@app.route('/testing')
def testing():
	return render_template('testing.html')
	
@app.route('/patient')
def patient():
	return render_template('patients.html')	
		

if __name__ == '__main__': 
    app.run(debug=True) #server will auto-restart when we save our changes to the code 
