from model.H1Query import H1Query
from flask import jsonify
from flask import render_template, request, make_response
from flask import Blueprint
from validation.Validator import *
import pickle

predict_blueprint = Blueprint('predict_blueprint', __name__, template_folder='templates')

@predict_blueprint.route('/predict',methods=['POST'])
def predict():
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
    info = {"patientid" : patient, "result":prediction,"age" : age, "sex" : gender, "cp":cp,"trestbps" : trestbps,"chol":chol,"fbs":fbs,"restecg":restecg,"thalach":thalach,"exang":exang,"oldpeak":oldpeak,"slope":slope,"ca":ca,"thal":thal}
    H1Query.insertH1Query(info)
    prediction = "Prediction : " + prediction +"."
    return render_template('index.html',prediction=prediction)