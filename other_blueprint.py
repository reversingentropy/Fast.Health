# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import jsonify
from flask import render_template, request, make_response
from flask import Blueprint
from jinja2 import TemplateNotFound
from validation.Validator import *

other_blueprint = Blueprint('other_blueprint', __name__, template_folder='templates')

#
# Other links
# 
#
# Other links
#
@other_blueprint.route('/aboutx')
def about():
    print('about page')
    return render_template('about.html')

@other_blueprint.route('/userx')
def user():
    print('user page')
    return render_template('users.html')
	
@other_blueprint.route('/testingx')
def testing():
    print('testing page')
    return render_template('testing.html')
	
@other_blueprint.route('/patientx')
def patientx():
    print('patient page')
    return render_template('patients.html')	

@other_blueprint.route('/shortcut', methods=['GET','POST'])
def shortcut():
    return render_template('index.html'),200

#
# Catch All
# 
@other_blueprint.route('/<string:page>')
def getPage(page):
    try:
        return render_template(page),200

    except TemplateNotFound:
        return render_template('404.html'),404
