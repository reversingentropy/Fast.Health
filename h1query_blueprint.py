# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import jsonify
from flask import render_template, request, make_response
from flask import Blueprint
from model.Params import Param
from model.H1Query import H1Query
from validation.Validator import *

h1query_blueprint = Blueprint('h1query_blueprint', __name__, template_folder='templates')

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
        jsonOutput = {'Rows Affected' : output}

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
            resp = make_response(render_template('', params=Param.QueryTableDeleteButton()),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401

    except Exception as err:
        print(err)
        return render_template('queries.html', params=Param.QueryTableDeleteButton()), 401
