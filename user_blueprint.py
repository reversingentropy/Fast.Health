# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import jsonify
from flask import render_template, request, make_response
from flask import Blueprint
from model.Params import Param
from model.User import User
from model.H1Query import H1Query
from model.Params import Param
from validation.Validator import *

user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates')
#
# Login Page
#
@user_blueprint.route('/')
def homepage():
    return render_template('login.html', params=Param.SetAllFalseParams()), 200

#
# User
#
@user_blueprint.route('/login', methods=['GET','POST'])
def loginpage():
    return render_template('login.html', params=Param.LoggingNoErrorParams()), 200

@user_blueprint.route('/registering', methods=['GET','POST'])
def registeringpage():
    return render_template('login.html', params=Param.RegisteringNoErrorParams()), 200

@user_blueprint.route('/changepass', methods=['GET','POST'])
def changingpage():
    return render_template('login.html', params=Param.ForgotNoErrorParams()), 200

@user_blueprint.route('/logout', methods=['GET','POST'])
def logout():
    resp = make_response(render_template("login.html", params=Param.SetAllFalseParams()),200)
    resp.delete_cookie('jwt')
    return resp

@user_blueprint.route('/user', methods=['GET'])
# @require_login
# @require_admin
def listallUsers(): # list all Users for select
    try:
        jsonUsers = User.getAllUsers()
        params = Param.UserTableNoButtons
        return render_template('users.html', results=jsonUsers, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging

@user_blueprint.route('/changeRoleUser', methods=['GET'])
# @require_login
# @require_admin
def gotoChangeRole(): # list all Users for select
    try:
        jsonUsers = User.getAllUsers()
        params = Param.UserTableChangeButton()
        return render_template('users.html', results=jsonUsers, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging
    
@user_blueprint.route('/deleteUser', methods=['GET'])
# @require_login
# @require_admin
def gotoDeleteUser(): # list all Users for select
    try:
        jsonUsers = User.getAllUsers()
        params = Param.UserTableDeleteButton()
        return render_template('users.html', results=jsonUsers, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging

@user_blueprint.route('/user', methods=['POST'])
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

@user_blueprint.route('/verifyUser', methods=['POST'])
def verifyUser():
    try:
        output = User.loginUser(request.form['email'], request.form['password'])
        if len(output['jwt']) > 0:
            # info = H1Query.initPredInfo()
            resp = make_response(render_template('index.html'),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('login.html', params=Param.LoggingWithErrorParams()), 401

    except Exception as err:
        print(err)
        return render_template('login.html', params=Param.LoggingWithErrorParams()), 401

@user_blueprint.route('/changePasswordUser', methods=['POST'])
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

@user_blueprint.route('/changeRoleUser/<int:userid>', methods=['POST'])
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

@user_blueprint.route('/deleteUser/<int:userid>', methods=['POST'])
# @require_login
# @require_admin
def deleteUser(userid):
    # whatever the case, return to the page with the data table
    try:
        output = User.deleteUser(userid)
        if len(output['jwt']) > 0:
            # info = H1Query.initPredInfo()
            resp = make_response(render_template('', params=Param.LoggingWithErrorParams()),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('', params=Param.LoggingWithErrorParams()), 401

    except Exception as err:
        print(err)
        return render_template('', params=Param.LoggingWithErrorParams()), 401