# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
# from model.DatabasePool import DatabasePool
from flask import session
from config.Settings import Settings
if Settings.dbUsed == 'pooling':
    from model.DatabasePool import DatabasePool
else:
    from model.DatabasePoolMySQL import DatabasePool
import datetime
import jwt
import bcrypt

class User:

    @classmethod
    def getAllUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM users;"
            cursor.execute(sql)
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
            print('release connection')
    
    @classmethod
    def insertUser(cls, username, email, role, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            # Hash a password for the first time, with a randomly generated salt
            passwordb = password.encode() # convert string to bytes
            hashed = bcrypt.hashpw(passwordb, bcrypt.gensalt())

            default_role = 'member' # purposely swapped for role

            sql = "INSERT INTO users (username, email, role, password) VALUES (%s, %s, %s, %s);"
            users = cursor.execute(sql, (username,
                                         email,
                                         default_role,
                                         hashed))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updateUserx(cls, username, email, password):
        try:
            print('updateUser ', username, email, password)
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            # Hash a password for the first time, with a randomly generated salt
            passwordb = password.encode() # convert string to bytes
            hashed = bcrypt.hashpw(passwordb, bcrypt.gensalt())

            sql = "UPDATE users SET password=%s WHERE username=%s AND email=%s;"
            users = cursor.execute(sql, (hashed,
                                         username,
                                         email))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updateUser(cls, userid, role):
        try:
            print('updateUser ', userid, role)
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "UPDATE users SET role=%s WHERE userid=%s;"
            users = cursor.execute(sql, (role,
                                         userid))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def deleteUser(cls, userid):
        if 'userid' in session:
            if session['userid'] != userid:
                try:
                    dbConn = DatabasePool.getConnection()
                    cursor = dbConn.cursor(dictionary=True)

                    sql = "DELETE FROM users WHERE userid=%s"
                    users = cursor.execute(sql, (userid,))
                    dbConn.commit()

                    rows = cursor.rowcount
                    return rows

                except:
                    print('Delete function error')
                    return -1
                finally:
                    dbConn.close()
                    print('release connection')
            else:
                return -1
        else:
            return -1

    @classmethod
    def loginUser(cls, email, password):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')

            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM users WHERE email=%s;"
            cursor.execute(sql, (email,))
            user = cursor.fetchone() # at most 1 record since email is supposed to be unique

            if user==None:
                return {'jwt' : ''}, -1 # No match
            else:
                # put password test over here
                storedpasswordb = user['password'].encode()
                plaintextb = password.encode()

                if (bcrypt.checkpw(plaintextb, storedpasswordb)):
                    payload = {'userid' : user['userid'],
                                'role' : user['role'],
                                'exp' : datetime.datetime.utcnow() +
                                        datetime.timedelta(seconds=7200)}
                    jwtToken = jwt.encode(payload, Settings.secretKey, algorithm="HS256")
                    # for Python 3, jwt.encode results in a byte string
                    # which is not accepted by flask.jsonify.
                    # Here the whole jwtToken is decoded to a string and posted in
                    # the bearer field of postman 
                    # jwtToken = jwtToken.decode('utf-8')
                    return {'jwt' : jwtToken}, user['userid']
                else:
                    return {'jwt' : ''}, -1 # No match

        finally:
            dbConn.close()
