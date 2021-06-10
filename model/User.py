from config.Settings import Settings
#from model.DatabasePool import DatabasePool
if Settings.dbUsed == 'maria':
    from model.DatabasePool import DatabasePool
else:
    from model.DatabasePoolMySQL import DatabasePool

import datetime
import jwt
import bcrypt
import secrets


class User:
    @classmethod
    def loginUser(cls,email, password): 
        try: 
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)

            print(f"Connected to {db_Info}");
            sql="select * from users where email=%s "

            print(email)
            cursor.execute(sql,(email,)) 
            user = cursor.fetchone()            
            username = ''
            print(user)
            if user == None:
                print('Empty listing')
                return {'jwt':'', 'username': username}
#            elif bcrypt.checkpw(password.encode(), user['password']):
            else:
#                print(user)
                hashed = user['password'].encode('utf8')
                password = password.encode('utf8')
                if bcrypt.checkpw(password, hashed):
                    print('password ok!')
                    userid = user['userid']
                    username = user['username']
                    payload = {"userid":user['userid'], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}
                    jwtToken=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                    return {"jwt":jwtToken, 'userid': userid, 'username': username}
                else:
                    print('Wrong password!')
                    return {'jwt': '', 'userid': 0, 'username': username}

        finally: 
            dbConn.close()
            print("release connection")


    @classmethod
    def getUser(cls,userid): 
        try: 
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)

            print(f"Connected to {db_Info}")
            sql="select * from users where userid=%s"

            cursor.execute(sql,(userid,)) 
            users = cursor.fetchone()
            return users

        finally: 
            dbConn.close()
            print("release connection")

    @classmethod
    def getAllUsers(cls): 
        try: 
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)

            print(f"Connected to {db_Info}");
            sql="select * from users; "

            cursor.execute(sql) 
            users = cursor.fetchall()
            return users

        finally: 
            dbConn.close()
            print("release connection")


    @classmethod
    def insertUser(cls,username, email, role, password):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

#            password=userJson["password"].encode() #convert string to bytes
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            default_role = 'member' # purposely swapped for role

            sql = "INSERT INTO users (username, email, role, password) VALUES (%s, %s, %s, %s);"
            users = cursor.execute(sql, (username,
                                         email,
                                         default_role,
                                         hashed))
            dbConn.commit()

            rows=cursor.rowcount
            return rows

        finally:
            dbConn.close()
            print('release connection')


    @classmethod
    def updateUser(cls, userid, user):

        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "update Users set "
            sql_field = ''
            item  = []
            for k, v in user.items():
                sql_field += k + ' = %s, ' 
                if k == 'password':
                    v = bcrypt.hashpw(v.encode(), bcrypt.gensalt())
                item.append(v)
            sql_field = sql_field.rstrip(', ')
            sql = sql + sql_field + ' where userid = %s'
            item.append(userid)
            users = cursor.execute(sql,item)

            dbConn.commit()
            rows=cursor.rowcount
            return rows

        finally:            
            dbConn.close()

    # @classmethod
    # def updateUser(cls, username, email, password):
    #     try:
    #         print('updateUser ', username, email, password)
    #         dbConn = DatabasePool.getConnection()
    #         cursor = dbConn.cursor(dictionary=True)

    #         # Hash a password for the first time, with a randomly generated salt
    #         passwordb = password.encode() # convert string to bytes
    #         hashed = bcrypt.hashpw(passwordb, bcrypt.gensalt())

    #         sql = "UPDATE users SET password=%s WHERE username=%s AND email=%s;"
    #         users = cursor.execute(sql, (hashed,
    #                                      username,
    #                                      email))
    #         dbConn.commit()

    #         rows = cursor.rowcount
    #         return rows
    #     finally:
    #         dbConn.close()
    #         print('release connection')

    # @classmethod
    # def updateUser(cls, userid, role):
    #     try:
    #         print('updateUser ', userid, role)
    #         dbConn = DatabasePool.getConnection()
    #         cursor = dbConn.cursor(dictionary=True)

    #         sql = "UPDATE users SET role=%s WHERE userid=%s;"
    #         users = cursor.execute(sql, (userid,
    #                                      role))
    #         dbConn.commit()

    #         rows = cursor.rowcount
    #         return rows
    #     finally:
    #         dbConn.close()
    #         print('release connection')

    @classmethod
    def deleteUser(cls,userid):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="delete from users where userid=%s"
            users = cursor.execute(sql,(userid,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        
        finally:
            dbConn.close()
            print('release connection')


    @classmethod
    def updatePassword(cls, email, password):
        try:        
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)
            
            sql = "update users set user.password=%s where user.email=%s"
            cursor.execute(sql,(password, email))
            dbConn.commit()

            rows=cursor.rowcount
            #return count
            return rows

        finally:
            dbConn.close()

    @classmethod
    def gen_password(cls, length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"):
        return "".join([secrets.choice(charset) for _ in range(0, length)])
#        return '12345678'

## Daneil's...

   



