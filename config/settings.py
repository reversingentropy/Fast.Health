import os

class Settings:

    secretKey="a12nc)238OmPq#cxOlm*a" 

    #Dev
    host='localhost'
    database='fasthealth'
    user='root'
    password='sum381Tk!'

    #Staging on heroku
    # host=os.environ['HOST']
    # database=os.environ['DATABASE']
    # user=os.environ['USERNAME']
    # password=os.environ['PASSWORD']

    # Pickle File
    pFile = './config/svm.pkl'
