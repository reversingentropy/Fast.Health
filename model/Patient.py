# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
# from model.DatabasePool import DatabasePool
from config.Settings import Settings
if Settings.dbUsed == 'pooling':
    from model.DatabasePool import DatabasePool
else:
    from model.DatabasePoolMySQL import DatabasePool

# import datetime
# import jwt
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
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
            print('release connection')
    
    @classmethod
    def insertPatient(cls, patientname, userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "INSERT INTO patients (patientname, userid) VALUES (%s, %s);"
            users = cursor.execute(sql, (patientname,
                                         userid))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updatePatient(cls, patientid, patientname, userid):
        try:
            print('updatePatient ', patientid, patientname, userid)
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "UPDATE patients SET patientname=%s, userid=%s WHERE patientid=%s;"
            users = cursor.execute(sql, (patientname,
                                         userid,
                                         patientid))
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
