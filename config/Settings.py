import os

class Settings:

    secretKey="a12nc)238OmPq#cxOlm*a" # your own secret key

    modelFile = "data/model.pkl" # machine learning model

    dbUsed = 'local'

    if dbUsed == 'local':
        #Staging on local machine
        host='localhost'
        database='fasthealth'
        user='root'
        password='sum381Tk!'

    else:
        #Staging on heroku
        host=os.environ['HOST']
        database=os.environ['DATABASE']
        user=os.environ['USERNAME']
        password=os.environ['PASSWORD']
