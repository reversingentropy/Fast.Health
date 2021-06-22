# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021
@author: Lenovo
"""
from datetime import date,datetime
from flask import json, session
from flask import render_template, request, make_response,jsonify,g,Blueprint
from model.Params import Param
from model.H1Query import H1Query
from validation.Validator import *
from model.Patient import Patient
from config.Settings import Settings
import pandas as pd
import os
import jwt
import pickle

h1query_blueprint = Blueprint(
    'h1query_blueprint', __name__, template_folder='templates')

#
# H1Query
#


@h1query_blueprint.route('/h1query', methods=['GET'])
@require_login
# @require_admin
def listallH1Queries():  # list all Patients for select

    try:
        patientid = request.args.get('patientid', default=-1)
        if g.role == 'admin':
            userid = -1
        else:
            userid = g.userid
        print('Userid : ', userid, ' Patientid:', patientid)
        jsonPatients = H1Query.getAllH1Queries(patientid, userid)
        
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableNoButtons()), 200

    except Exception as err:
        print(err)  # for debugging
        return render_template('queries.html', params=Param.QueryTableNoButtons()), 500



@h1query_blueprint.route('/changeH1Query', methods=['GET'])
@require_login
def gotoUpdateH1Queries():
    try:
        jsonPatients = H1Query.getAllH1Queries()
        
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableUpdateButton()), 200

    except Exception as err:
        print(err)  # for debugging


@h1query_blueprint.route('/changeH1Query/<int:queryid>', methods=['POST'])
@require_login
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
@require_login
# @require_admin
def gotoDeleteH1Query():
    try:
        jsonPatients = H1Query.getAllH1Queries()
        return render_template('queries.html', info=jsonPatients, params=Param.QueryTableDeleteButton()), 200

    except Exception as err:
        print(err)  # for debugging


@h1query_blueprint.route('/deleteH1Query/<int:queryid>', methods=['GET'])
@require_login
# @require_admin
def deleteH1Query(queryid):
    # whatever the case, return to the page with the data table
    try:
        #print("deleteH1Query ", queryid)
        output = H1Query.deleteH1Query(queryid)
        if output > 0:
            jsonH1Queries = H1Query.getAllH1Queries()
            params = Param.QueryTableDeleteButton()
            resp = make_response(render_template(
                'queries.html', params=params, info=jsonH1Queries), 200)
            return resp

        else:
            return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401

    except Exception as err:
        print(err)
        return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401

@h1query_blueprint.route('/hd',methods=['GET'])
@require_login
# @require_admin
def display():
    auth_token=request.cookies.get("jwt")
    payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
    g.userid = payload['userid']
    pats = Patient.getAllPatients(userid= g.userid)
    if len(pats)==0:
        return render_template('indexEmpty.html')
    else:
        return render_template('index.html',pats=pats)

@h1query_blueprint.route('/predict',methods=['POST'])
@require_login
# @require_admin
def predict():
    auth_token=request.cookies.get("jwt")
    payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
    g.userid = payload['userid']
    pats = Patient.getAllPatients(userid= g.userid)
    if len(pats)==0:
        return render_template('indexEmpty.html')
    else:
        new_model = pickle.load(open(Settings.modelFile, 'rb'))
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

@h1query_blueprint.route('/batchhd',methods=['GET','POST'])
@require_login
# @require_admin
def batchdisplay():

    return render_template('batchprediction.html', info=[]), 200

def blockpredict(patientids, df):
    print('Loading machine learning model...')
    f = open(Settings.modelFile, 'rb')
    new_model = pickle.load(f)
    f.close()

    print(f'blockpredict with {len(df)} records')
    recordList = []
    for i in range(len(df)):
        if df['patientid'][i] in patientids:
            age = int(df['age'][i])
            sex = int(df['sex'][i])
            cp = int(df['cp'][i])
            trestbps = int(df['trestbps'][i])
            chol = int(df['chol'][i])
            fbs = int(df['fbs'][i])
            restecg = int(df['restecg'][i])
            thalach = int(df['thalach'][i])
            exang = int(df['exang'][i])
            oldpeak = float(df['oldpeak'][i])
            slope = int(df['slope'][i])
            ca = int(df['ca'][i])
            thal = int(df['thal'][i])
            data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            y_pred = new_model.predict([data])
            result = float(y_pred[0])
            patientid = int(df['patientid'][i])
            data.insert(0, result)
            data.insert(0, patientid)
            record = tuple(data)
            recordList.append(record)
            print('{} of {}'.format(i+1, len(df)))
    H1Query.insertBlockH1Query(recordList)
    return

@h1query_blueprint.route('/batchloadpredict',methods=['POST'])
@require_login
# @require_admin
def batchloadpredict():
    userid = session['userid']

    extensions = ['.csv']
    fpath = request.files['file']
    print('File path is ', fpath.filename)
    _, fext = os.path.splitext(fpath.filename)
    if not fext in extensions:
        print('File path has the wrong extension.')
        return render_template('batchprediction.html', info=[]), 500

    patients = Patient.getAllPatients(userid=userid)
    patientids = [int(patient['patientid']) for patient in patients]

    df = pd.read_csv(fpath)
    print('Number of records :', len(df))
    maxrecords = 100
    if len(df) > maxrecords:
        print(f'Restricted to {maxrecords} records.')
        return render_template('batchprediction.html', info=[]), 500

    blockpredict(patientids, df)
    # thread = Thread(target=blockpredict, kwargs={'patientids': patientids, 'df':df})
    # thread.start()

    jsondf = json.loads(df.to_json(orient='records'))
    return render_template('batchprediction.html', info=jsondf), 200

