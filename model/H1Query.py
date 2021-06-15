# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
from config.Settings import *
if Settings.dbUsed == 'pooling':
    from model.DatabasePool import DatabasePool
else:
    from model.DatabasePoolMySQL import DatabasePool

from datetime import datetime

class H1Query:

    # @classmethod
    # def initPredInfo(cls):
    #     info = {}
    #     info['userid'] = -1
    #     info['sepalLength'] = 0.000
    #     info['sepalWidth'] = 0.000
    #     info['petalLength'] = 0.000
    #     info['petalWidth'] = 0.000
    #     info['prediction'] = 'Unknown'
    #     info['InsertionDate'] = datetime.now()

    #     return info

    @classmethod
    def initH1Query(cls):
        h1q = {}
        h1q['patientid'] = 0
        h1q['result'] = 0.0
        h1q['age'] = 0
        h1q['sex'] = 0
        h1q['cp'] = 0
        h1q['trestbps'] = 0
        h1q['chol'] = 0
        h1q['fbs'] = False
        h1q['restecg'] = 0
        h1q['thalach'] = 0
        h1q['exang'] = False
        h1q['oldpeak'] = 0.0
        h1q['slope'] = 0
        h1q['ca'] = 0
        h1q['thal'] = 0

        return h1q

    @classmethod
    def getAllH1Queries(cls, patientid=-1):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            if patientid==-1:
                sql = "SELECT * FROM h1queries;"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM h1queries WHERE userid=%s;"
                cursor.execute(sql,(patientid,))
            h1queries = cursor.fetchall()
            return h1queries
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def insertH1Query(cls, info):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "INSERT INTO h1queries (patientid,result,age,sex,cp,trestbps,chol,fbs, \
                restecg,thalach,exang,oldpeak,slope,ca,thal) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            users = cursor.execute(sql, (info['patientid'],
                                         info['result'],
                                         info['age'],
                                         info['sex'],
                                         info['cp'],
                                         info['trestbps'],
                                         info['chol'],
                                         info['fbs'],
                                         info['restecg'],
                                         info['thalach'],
                                         info['exang'],
                                         info['oldpeak'],
                                         info['slope'],
                                         info['ca'],
                                         info['thal']))
            dbConn.commit()

            # rows = cursor.rowcount
            lastInsertId = cursor.lastrowid
            return lastInsertId
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updateH1Query(cls, queryid, patientid):
        try:
            print('updateH1Query ', queryid, patientid)
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "UPDATE h1queries SET patientid=%s WHERE queryid=%s;"
            users = cursor.execute(sql, (patientid,))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def deleteH1Query(cls, queryid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE FROM h1queries WHERE queryid=%s;"
            users = cursor.execute(sql, (queryid,))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

