# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import Flask, jsonify
from flask import render_template, make_response
from flask_cors import CORS
from datetime import datetime
from config.Settings import Settings
from model.Params import Param
from validation.Validator import *
from user_blueprint import user_blueprint
from patient_blueprint import patient_blueprint
from h1query_blueprint import h1query_blueprint
from other_blueprint import other_blueprint
from predict_blueprint import predict_blueprint

import os, pickle

app = Flask(__name__, template_folder='templates')
# CORS(app) # to enable CORS middleware for all origins

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

app.register_blueprint(user_blueprint)
app.register_blueprint(patient_blueprint)
app.register_blueprint(h1query_blueprint)
app.register_blueprint(other_blueprint)
app.register_blueprint(predict_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
