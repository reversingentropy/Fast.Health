# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021
@author: Lenovo
"""
from flask import render_template, request, make_response
from flask import Blueprint
from model.Params import Param
from model.H1Query import H1Query
from validation.Validator import *
from model.H1Query import H1Query
from model.Patient import Patient
from config.Settings import Settings
import jwt
from flask import jsonify,g
import pickle

h1query_blueprint = Blueprint(
    'h1query_blueprint', __name__, template_folder='templates')

#
# H1Query
#


@h1query_blueprint.route('/h1query', methods=['GET'])
# @require_login
# @require_admin
def listallH1Queries():  # list all Patients for select
    try:
        jsonPatients = H1Query.getAllH1Queries()
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableNoButtons()), 200

    except Exception as err:
        print(err)  # for debugging


@h1query_blueprint.route('/changeH1Query', methods=['GET'])
def gotoUpdateH1Queries():
    try:
        jsonPatients = H1Query.getAllH1Queries()
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableUpdateButton()), 200

    except Exception as err:
        print(err)  # for debugging


@h1query_blueprint.route('/changeH1Query/<int:queryid>', methods=['POST'])
# @require_login
# @require_admin
def updateH1Queries(queryid):
    try:
        output = H1Query.updateH1Query(queryid)
        jsonOutput = {'Rows Affected': output}

        if output > 0:
            return render_template('queries.html', params=Param.QueryTableUpdateButton()), 201

        else:
            return render_template('queries.html', params=Param.QueryTableUpdateButton()), 500

    except Exception as err:
        print(err)
        return render_template('queries.html', params=Param.QueryTableUpdateButton()), 500


@h1query_blueprint.route('/deleteH1Query', methods=['GET'])
# @require_login
# @require_admin
def gotoDeleteH1Query():
    try:
        jsonPatients = H1Query.getAllH1Queries()
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableDeleteButton()), 200

    except Exception as err:
        print(err)  # for debugging


@h1query_blueprint.route('/deleteH1Query/<int:queryid>', methods=['POST'])
# @require_login
# @require_admin
def deleteH1Query(queryid):
    # whatever the case, return to the page with the data table
    try:
        output = H1Query.deleteH1Query(queryid)
        if len(output['jwt']) > 0:
            # info = H1Query.initPredInfo()
            resp = make_response(render_template(
                '', params=Param.QueryTableDeleteButton()), 200)
            # writes instructions in the header for browser to save a cookie to browser for the jwt
            resp.set_cookie('jwt', output["jwt"])
            return resp

        else:
            return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401

    except Exception as err:
        print(err)
        return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401



@h1query_blueprint.route('/hd',methods=['GET'])
# @require_login
# @require_admin
def display():
    auth_token=request.cookies.get("jwt")
    payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
    g.userid = payload['userid']
    pats = Patient.getAllPatients(userid= g.userid)
    print(pats)
    if len(pats)==0:
        return render_template('indexEmpty.html')
    else:
        return render_template('index.html',pats=pats)

@h1query_blueprint.route('/predict',methods=['POST'])
# @require_login
# @require_admin
def predict():
    auth_token=request.cookies.get("jwt")
    payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
    g.userid = payload['userid']
    pats = Patient.getAllPatients(userid= g.userid)
    if len(pats)==0:
        return render_template('indexEmpty.html')
    else:
        new_model = pickle.load(open("data\model.pkl", 'rb'))
        patient = int(request.form['pId'])
        age = int(request.form['age'])
        gender = int(request.form['gender'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['rbp'])
        chol = int(request.form['chol'])
        if 'fbs' in request.form: 
            fbs = 1
        else:
            fbs = 0
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        if 'exang' in request.form: 
            exang = 1
        else:
            exang = 0
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca =  int(request.form['ca'])
        thal =  int(request.form['thal'])
        data = [age,gender,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        y_pred= new_model.predict([data])
        prediction = ["No Heart Disease","Heart Disease"][(y_pred[0])]
        num = int((y_pred[0]))
        info = {"patientid" : patient, "result":num,"age" : age, "sex" : gender, "cp":cp,"trestbps" : trestbps,"chol":chol,"fbs":fbs,"restecg":restecg,"thalach":thalach,"exang":exang,"oldpeak":oldpeak,"slope":slope,"ca":ca,"thal":thal}
        H1Query.insertH1Query(info)
        prediction = "Prediction : " + prediction +"."
        return render_template('index.html',prediction=prediction,pats=pats)