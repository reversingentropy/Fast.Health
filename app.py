from flask import Flask, jsonify, abort
from flask import render_template, request, make_response, g
from flask_cors import CORS
from jinja2 import TemplateNotFound

from datetime import datetime
from config.Settings import Settings
from model.Params import Param
from model.User import User
from model.Patient import Patient
from model.H1Query import H1Query
from validation.Validator import *
import bcrypt
import os, pickle
import numpy as np


#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

params = Param.SetAllFalseParams()
model = None
if os.path.isfile(Settings.modelFile):
    print('Model file found. Loading model .....')
    model = pickle.load(open(Settings.modelFile, 'rb'))
    
else:
    print('Model file not found. Model not loaded.')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Login
#
# Modals about Login In/Out
#
@app.route('/login', methods=['GET','POST'])
def loginpage():
    return render_template('login.html', params=Param.LoggingNoErrorParams()), 200

@app.route('/registering', methods=['GET','POST'])
def registeringpage():
    return render_template('login.html', params=Param.RegisteringNoErrorParams()), 200

@app.route('/changepass', methods=['GET','POST'])
def changingpage():
    return render_template('login.html', params=Param.ForgotNoErrorParams()), 200

@app.route('/logout', methods=['GET','POST'])
def logout():
    resp = make_response(render_template("login.html", params=Param.SetAllFalseParams()),200)
    resp.delete_cookie('jwt')
    return resp

@app.route('/shortcut', methods=['GET','POST'])
def shortcut():
    return render_template('index.html'),200


# @app.route('/login', methods=['POST'])
# def verifyUser():
#     try:
#         email = request.form['email']
#         password = request.form['pwd']
#         print(email, password)
#         ret = User.loginUser(email, password)
#         token = ret['jwt']
#         userid = ret['userid']
#         username = ret['username']
#         if len(token) > 0:
#             results = Iris_DB.getAllPrediction(userid)
#             resp = make_response(render_template('mainPage.html', username= username, results=results, prediction=""))
#             resp.set_cookie('jwt', token)
#             return resp, 200
#         else:
#             resp = make_response(render_template('login.html',  message='Invalid Login Credentials!'))
#             resp.set_cookie('jwt', '')
#             return resp, 404
#     except Exception as err:
#         print(err) #for debugging 
#         message = 'Invalid Login Credentials!'
#         resp = make_response(render_template('login.html',  message=message))
#         return resp, 404


@app.route('/')
def homepage():
    return render_template('login.html', params=Param.SetAllFalseParams()), 200

@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/userlist', methods=["GET"])
def userlist():
    try:
        res = User.getAllUsers()
#        jsonUsers = {'Users' : jsonUsers}
        print(res)
        return render_template('users.html', results = res), 200

    except Exception as Err:
        print (Err)
        return abort(404)

@app.route('/user', methods=['GET'])
# @require_login
# @require_admin
def listallUsers(): # list all Users for select
    try:
        jsonUsers = User.getAllUsers()
        jsonUsers = {'Users' : jsonUsers}

        info = jsonify(jsonUsers)
        return render_template('', info=info), 200
    
    except Exception as err:
        print(err)  # for debugging    
    
@app.route('/user', methods=['POST'])
@validateRegister
def insertUser():
    username = request.form['usernamer']
    email = request.form['emailr']
    role = request.form['roler']
    password = request.form['passwordr']
    password1 = request.form['passwordr1']

    if (password == password1):
        try:        
            output = User.insertUser(username, email, role, password)
            jsonOutput = {'Rows Affected' : output}
            return render_template('login.html', params=Param.SetAllFalseParams()), 201

        except Exception as err:
            print(err)
            return render_template('login.html', params=Param.RegisteringWithErrorParams()), 500

    else:   # password != password1
        return render_template('login.html', params=Param.RegisteringWithErrorParams()), 500

# @app.route('/user', methods=['GET'])
# # @require_login
# # @require_admin
# def listallUsers(): # list all Users for select
#     try:
#         jsonUsers = User.getAllUsers()
#         jsonUsers = {'Users' : jsonUsers}

#         info = jsonify(jsonUsers)
#         return render_template('', info=info), 200
    
#     except Exception as err:
#         print(err)  # for debugging    


@app.route('/testing')
def testing():
	return render_template('testing.html')
	
@app.route('/patient')
def patient():
	return render_template('patients.html')	
		
# @app.route('/user', methods=['POST'])
# @validateRegister
# def insertUser():
#     username = request.form['usernamer']
#     email = request.form['emailr']
#     role = request.form['roler']
#     password = request.form['passwordr']
#     password1 = request.form['passwordr1']

#     if (password == password1):
#         try:        
#             output = User.insertUser(username, email, role, password)
#             jsonOutput = {'Rows Affected' : output}
#             return render_template('login.html', params=Param.SetAllFalseParams()), 201

#         except Exception as err:
#             print(err)
#             return render_template('login.html', params=Param.RegisteringWithErrorParams()), 500

#     else:   # password != password1
#         return render_template('login.html', params=Param.RegisteringWithErrorParams()), 500

@app.route('/verifyUser', methods=['POST'])
def verifyUser():
    try:
        output = User.loginUser(request.form['email'], request.form['password'])
        if len(output['jwt']) > 0:
            info = H1Query.initPredInfo()
            resp = make_response(render_template('index.html'),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('login.html', params=Param.LoggingWithErrorParams()), 401

    except Exception as err:
        print(err)
        return render_template('login.html', params=Param.LoggingWithErrorParams()), 401

@app.route('/changePasswordUser', methods=['POST'])
@validatePassword
def updateUser():
    username = request.form['usernamef']
    email = request.form['emailf']
    password = request.form['passwordf']
    password1 = request.form['passwordf1']

    if (password == password1):
        try:        
            output = User.updateUser(username, email, password)
            jsonOutput = {'Rows Affected' : output}

            if output > 0:
                return render_template('login.html', params=Param.SetAllFalseParams()), 201
                                        
            else:
                return render_template('login.html', params=Param.ForgotWithErrorParams()), 500

        except Exception as err:
            print(err)
            return render_template('login.html', params=Param.ForgotWithErrorParams()), 500

    else:   # password != password1
        return render_template('login.html', params=Param.ForgotWithErrorParams()), 500

@app.route('/changeRoleUser/<int:userid>', methods=['POST'])
# @require_login
# @require_admin
def changeroleUser(userid):
    try:        
        output = User.updateUser(userid, 'user')
        jsonOutput = {'Rows Affected' : output}

        if output > 0:
            return render_template('', params=Param.SetAllFalseParams()), 201
                                    
        else:
            return render_template('', params=Param.ForgotWithErrorParams()), 500

    except Exception as err:
        print(err)
        return render_template('', params=Param.ForgotWithErrorParams()), 500

@app.route('/deleteUser/<int:userid>', methods=['POST'])
# @require_login
# @require_admin
def deleteUser(userid):
    # whatever the case, return to the page with the data table
    try:
        output = User.deleteUser(userid)
        if len(output['jwt']) > 0:
            info = H1Query.initPredInfo()
            resp = make_response(render_template('', params=Param.LoggingWithErrorParams()),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('', params=Param.LoggingWithErrorParams()), 401

    except Exception as err:
        print(err)
        return render_template('', params=Param.LoggingWithErrorParams()), 401

#
# Patient
#
@app.route('/patient', methods=['GET'])
# @require_login
# @require_admin
def listallPatients():  # list all Patients for select
    try:
        jsonPatients = Patient.getAllPatients()
        jsonPatients = {'Patients' : jsonPatients}

        info = jsonify(jsonPatients)
        return render_template('', info=info), 200
    
    except Exception as err:
        print(err)  # for debugging

@app.route('/patient', methods=['POST'])
# @require_login
def insertPatient():
    patientname = request.form['patientname']
    userid = request.form['userid']

    try:        
        output = Patient.insertPatient(patientname, userid)
        jsonOutput = {'Rows Affected' : output}
        return render_template('', params=Param.SetAllFalseParams()), 201

    except Exception as err:
        print(err)
        return render_template('', params=Param.RegisteringWithErrorParams()), 500


@app.route('/changePatient/<int:patientid>', methods=['POST'])
# @require_login
# @require_admin
def updatePatient(patientid):
    try:
        output = Patient.updatePatient(patientid)
        jsonOutput = {'Rows Affected' : output}

        if output > 0:
            return render_template('', params=Param.SetAllFalseParams()), 201
                                    
        else:
            return render_template('', params=Param.ForgotWithErrorParams()), 500

    except Exception as err:
        print(err)
        return render_template('', params=Param.ForgotWithErrorParams()), 500

@app.route('/deletePatient/<int:patientid>', methods=['POST'])
# @require_login
# @require_admin
def deletePatient(patientid):
    # whatever the case, return to the page with the data table
    try:
        output = Patient.deletePatient(patientid)
        if len(output['jwt']) > 0:
            info = H1Query.initPredInfo()
            resp = make_response(render_template('', params=Param.LoggingWithErrorParams()),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('', params=Param.LoggingWithErrorParams()), 401

    except Exception as err:
        print(err)
        return render_template('', params=Param.LoggingWithErrorParams()), 401

#
# Catch All
# 
@app.route('/<string:page>')
def getPage(page):
    try:
        return render_template(page),200

    except TemplateNotFound:
        return render_template('404.html'),404


if __name__ == '__main__': 
    app.run(debug=True) #server will auto-restart when we save our changes to the code 
