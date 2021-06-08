from model.DatabasePool import DatabasePool
from config.settings import Settings
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
            sql="select * from user where email=%s "

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
#            print("release connection")

    @classmethod
    def getUser(cls,userid): 
        try: 
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)

            print(f"Connected to {db_Info}")
            sql="select * from user where userid=%s"

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
            sql="select * from user "

            cursor.execute(sql) 
            users = cursor.fetchall()
            return users

        finally: 
            dbConn.close()
            print("release connection")

    @classmethod
    def insertUser(cls,username, email, password):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

#            password=userJson["password"].encode() #convert string to bytes
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            sql="insert into user(username,email,password) Values(%s,%s,%s)"
            users = cursor.execute(sql,(username, email, hashed))

            dbConn.commit()

            rows=cursor.rowcount
            return rows

        finally:
            dbConn.close()


    @classmethod
    def updateUser(cls, userid, user):

        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "update User set "
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

    @classmethod
    def deleteUser(cls,userid):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="delete from user where userid=%s"
            users = cursor.execute(sql,(userid,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        
        finally:
            dbConn.close()

    @classmethod
    def updatePassword(cls, email, password):
        try:        
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            cursor = dbConn.cursor(dictionary=True)
            
            sql = "update user set user.password=%s where user.email=%s"
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
