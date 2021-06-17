# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
# from model.DatabasePool import DatabasePool
from config.Settings import Settings
from flask import g
if Settings.dbUsed == 'pooling':
    from model.DatabasePool import DatabasePool
else:
    from model.DatabasePoolMySQL import DatabasePool

# import datetime
import jwt
# import bcrypt

class Patient:

    @classmethod
    def getAllPatients(cls, userid=-1): # -1 to show all
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            if userid==-1:
                sql = "SELECT * FROM patients;"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM patients WHERE userid=%s"
                cursor.execute(sql, (userid,))
            patients = cursor.fetchall()
            return patients
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def getPatientInfo(cls, patientid):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM patients WHERE patientid=%s"
            cursor.execute(sql, (patientid,))
            patient_dict = cursor.fetchone()
            print(patient_dict)
            return patient_dict
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def insertPatient(cls, patient_dict):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            p = patient_dict
            sql = "INSERT INTO patients (patientname, userid, nricno, contactno, address, gender, age, email, dob, postcode)   \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            print(sql)
            users = cursor.execute(sql, (p['name'], p['userid'], p['nricno'], p['contactno'], p['address'], p['gender'], p['age'], 
                    p['email'], p['dob'], p['postcode']))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updatePatient(cls, patientid, patient_dict):
        try:
#            print('updatePatient ', patientid, patientname, userid)
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            p = patient_dict
            sql = "UPDATE patients SET patientname=%s, nricno=%s, contactno = %s, address=%s, gender=%s, age=%s, email=%s, dob=%s, postcode=%s \
                   WHERE patientid=%s;"
            users = cursor.execute(sql, (p['name'], p['nricno'], p['contactno'], p['address'], p['gender'], p['age'], p['email'], p['dob'], p['postcode'], patientid))
            print(sql)
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def deletePatient(cls, patientid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE FROM patients WHERE patientid=%s"
            users = cursor.execute(sql, (patientid,))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def InitVal(cls, userid):
        return {'userid':userid, 'patientid': -1, 'name':'', 'gender':'', 'nricno':'', 'email':'', 
                'age':0, 'dob':'', 'address':'', 'contactno':'', 'postcode':''}

    @classmethod
    def getUserID(cls, request):
        try:
            auth_token=request.cookies.get("jwt")
            payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
            g.userid = payload['userid'] # update info in flask application context's g which lasts for one req/res cycle
            g.role = payload['role']
            return g.userid
        except Exception as err:
            print(err)
            g.userid = 0
