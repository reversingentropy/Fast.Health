# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import jsonify
from flask import render_template, request, make_response, abort, g
from flask import Blueprint
from model.Params import Param
from model.Patient import Patient
from model.H1Query import H1Query
from validation.Validator import *

patient_blueprint = Blueprint('patient_blueprint', __name__, template_folder='templates')

#
# Patient
#


@patient_blueprint.route('/listallpatients', methods=['GET'])
# @require_login
# @require_admin
def listallpatients():  # list all Patients for select
    try:
        userid = Patient.getUserID(request)
#        userid = g.userid
        role = g.role
        print('User ID: ', userid, ' Role:', role)
        if role == 'admin':
            userid = -1        
        jsonPatients = Patient.getAllPatients(userid)
        params = Param.PatientsTableDefButton()

#        info = jsonify(jsonPatients)
        return render_template('patients.html', results=jsonPatients, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging
        return render_template('patients.html', params=Param.PatientsTableDefButton()), 500

@patient_blueprint.route('/insert_patients')
# @require_login
def newPatient():
    userid = Patient.getUserID(request)
    print(userid)
    patient_dict= Patient.InitVal(userid)
    return render_template('insupd_patients.html', message='New Patient', action='insert', patient_dict=patient_dict), 200


@patient_blueprint.route('/patient', methods=['POST'])
# @require_login
def insupdPatient():
    userid = Patient.getUserID(request)
    action = request.form['action']
    print('Action=', action)

    patient_dict = {'userid': userid,
                    "name": request.form['name'], 
                     "gender": request.form['gender'],
                     "age": request.form['age'],
                     "dob": request.form['dob'],
                     "nricno": request.form['nricno'],
                     "email": request.form['email'],
                     "contactno": request.form['contactno'],
                     "address": request.form['address'],
                     "postcode": request.form['postcode']}
    print(patient_dict)
    try:  
        if action == 'insert':  # Insert
            output = Patient.insertPatient(patient_dict)
            msgOutput = 'Rows Affected=' + str( output )
            return render_template('insupd_patients.html', params=Param.SetAllFalseParams(), action=action, message='Status: '+ msgOutput, patient_dict=Patient.InitVal(userid)), 201

        else: # Update
            patientid = int(request.form['patientid'])
            print('PatID:', patientid)
            output = Patient.updatePatient(patientid, patient_dict)
            msgOutput =  str( output ) + ' record updated.'
            jsonPatients = Patient.getAllPatients(userid)
            params = Param.PatientsTableUpdateButton()
            return render_template('patients.html', results=jsonPatients, params=params, action=action, message=msgOutput), 200

    except Exception as err:
        print(err)
        return render_template('insupd_patients.html', params=Param.RegisteringWithErrorParams(), action=action, message=err, patient_dict=Patient.InitVal(userid)), 500

@patient_blueprint.route('/updatePatient/<int:patientid>', methods=['GET'])
# @require_login
# @require_admin
def updatePatient(patientid):
    try:
        print('Patiend ID:', patientid)
        ## Display list of Patient particulars
        patient_dict = Patient.getPatientInfo(patientid)
        patient_dict['dob'] = patient_dict['dob'].strftime('%Y-%m-%d')
        print(patient_dict)
        if patient_dict:
#        output = Patient.updatePatient(patientid)
#        jsonOutput = {'Rows Affected' : output}
            return render_template('insupd_patients.html', params=Param.SetAllFalseParams(), action='update', patient_dict=patient_dict, message=''), 201
                                        
        else:
            # Error retrieve info
            messaage='Patient record not found!'
            return render_template('patients.html', params=Param.PatientsTableDefButton(), message=message), 500

    except Exception as err:
        print(err)
        return render_template('patients.html', params=Param.PatientsTableDefButton(), message=err), 500

@patient_blueprint.route('/deletePatient/<int:patientid>', methods=['GET'])
# @require_login
# @require_admin
def deletePatient(patientid):
    # whatever the case, return to the page with the data table
    try:
        userid = Patient.getUserID(request)
        print(patientid)
        output = Patient.deletePatient(patientid)
        if output > 0:
            ret = 200
        else:
            ret = 401
        msgOutput = str(output) + ' record deleted.'
            # Display list of patients            
        jsonPatients = Patient.getAllPatients(userid)
        params = Param.PatientsTableDeleteButton()
        resp = make_response(render_template('patients.html', params=params, results=jsonPatients, message=msgOutput),ret)
#        resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
        return resp

    except Exception as err:
        print(err)
        jsonPatients = Patient.getAllPatients(userid)
        params = Param.PatientsTableDeleteButton()
        msgOutput = "Error to delete patient with ID " + str(patientid)
        resp = make_response(render_template('patients.html', params=params, results=jsonPatients, message=msgOutput), 401)
#        return render_template('patients.html', params=Param.LoggingWithErrorParams()), 401
        return resp


@patient_blueprint.route('/update_patients', methods=['GET'])
def gotoupdtepatient(): # list all Users for select
    try:
        userid = Patient.getUserID(request)
        role = g.role
        print('User ID: ', userid, ' Role:', role)
        if role == 'admin':
            userid = -1        
        jsonPatients = Patient.getAllPatients(userid =userid)
        params = Param.PatientsTableUpdateButton()
        return render_template('patients.html', results=jsonPatients, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging
        abort(404)

@patient_blueprint.route('/delete_patients', methods=['GET'])
def gotodeletepatient(): # list all Users for select
    try:
        userid = Patient.getUserID(request)
        role = g.role
        print('User ID: ', userid, ' Role:', role)
        if role == 'admin':
            userid = -1        
        jsonPatients = Patient.getAllPatients(userid = userid)
        params = Param.PatientsTableDeleteButton()
        return render_template('patients.html', results=jsonPatients, params=params), 200
    
    except Exception as err:
        print(err)  # for debugging
        abort(404)
