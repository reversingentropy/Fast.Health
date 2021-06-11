# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import jsonify
from flask import render_template, request, make_response
from flask import Blueprint
from model.Params import Param
from model.Patient import Patient
from model.H1Query import H1Query
from validation.Validator import *

patient_blueprint = Blueprint('patient_blueprint', __name__, template_folder='templates')

#
# Patient
#
@patient_blueprint.route('/patient', methods=['GET'])
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

@patient_blueprint.route('/patient', methods=['POST'])
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

@patient_blueprint.route('/changePatient/<int:patientid>', methods=['POST'])
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

@patient_blueprint.route('/deletePatient/<int:patientid>', methods=['POST'])
# @require_login
# @require_admin
def deletePatient(patientid):
    # whatever the case, return to the page with the data table
    try:
        output = Patient.deletePatient(patientid)
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