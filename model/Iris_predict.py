from model.DatabasePool import DatabasePool
from config.settings import Settings
from sklearn import svm
import pickle


class Iris_SVC:
#    load_SVC_Model = pickle.load( open('config\svm.pkl', "rb" ) ) 

    @classmethod
    def Predict(cls, predict_param): 
        load_SVC_Model = pickle.load( open(Settings.pFile, "rb" ) ) 
        ret = load_SVC_Model.predict(predict_param)
        return ret
        

class Iris_DB:

    @classmethod
    def InsertDB(cls, predict_param, result, userid):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="insert into irisprediction (userid, sepalLength, sepalWidth, petalLength, petalWidth, prediction) values (%s, %s, %s, %s, %s, %s)"
            users = cursor.execute(sql,(userid, predict_param[0],  predict_param[1], predict_param[2],  predict_param[3], result))

            dbConn.commit()

            rows=cursor.rowcount
            return rows

        finally:
            dbConn.close()
        
    @classmethod
    def getAllPrediction(cls, userid):
        try:
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)

            sql="select * from irisprediction where userid = %s"
            cursor.execute(sql,(userid,)) 

            results = cursor.fetchall()
            return results

        finally: 
            dbConn.close()


        
    @classmethod
    def RemoveDB(cls, predictionId):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="delete from irisprediction where predictionId=%s"
            users = cursor.execute(sql,(predictionId,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        
        finally:
            dbConn.close()

