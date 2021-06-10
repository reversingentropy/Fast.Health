import functools
from flask import Flask,jsonify,request,g, redirect, make_response, render_template
from config.Settings import Settings
from model.Params import Param

import jwt
import re


def require_login(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        auth = True
        auth_token=request.cookies.get("jwt")

        if auth_token == None:
            auth = False
        if auth_token:
            try:
                print('auth_token found')
                # auth_token = auth_token.encode('utf-8')
                payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
                g.userid = payload['userid'] # update info in flask application context's g which lasts for one req/res cycle
                g.role = payload['role']

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth = False # Failed check

        if auth==False:
            return render_template('login.html', params=Param.LoggingWithErrorParams()), 401
        return func(*args, **kwargs)
    
    return secure_login

def login_required(func):
    @functools.wraps(func)
    def checkLogin(*args, **kwargs):
        auth = True
#        auth_header = request.headers.get('Authorization') #retrieve authorization bearer token
        auth_header = request.cookies.get("jwt")
        if auth_header == '':
            auth=False #Failed check
        else:
            try:
                payload = jwt.decode(auth_header,Settings.secretKey,algorithms=['HS256'])
#                print(payload)
                g.userid=payload['userid']#update info in flask application context's g which lasts for one req/res cyycle
#                g.role=payload['role']
                print('User:', g.userid)

            except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError) as err:
                print(err)
                auth=False #Failed check
            except Exception as err2:
                print(err2)
                auth=False #Failed check

        if auth==False:
            message = "Not Authorized!"
#            return redirect('login.html?message=%s' % message)
            resp = make_response(render_template('login.html',  message=message))
            resp.set_cookie('jwt', '')
            return resp, 404

        return func(*args, **kwargs)

    return checkLogin

def require_admin(func):
    @functools.wraps(func)
    def secure_admin(*args, **kwargs):
        auth = True
        if g.role != 'admin':
            auth = False

        if auth==False:
            return jsonify({'Message' : 'Not Authorized!'}),401 # return response

        return func(*args, **kwargs)
    
    return secure_admin



def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def secure_adminorself(*args, **kwargs):
        auth = True

        if g.role != 'admin' and g.userid != kwargs['userid']:
            auth = False # Failed check

        if auth==False:
            return jsonify({'Message' : 'Not Authorized!'}),401 # return response

        return func(*args, **kwargs)
    
    return secure_adminorself


## Validate User Info b4 Insert
def validateRegister(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        username = request.form['usernamer']
        email = request.form['emailr']
        role = request.form['roler']
        password = request.form['passwordr']

        patternUsername = re.compile('^[a-zA-Z0-9_. -]+$')
        # patternEmail = re.compile('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+@\w+\.\w+$')
        patternEmail = re.compile('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.]+$')
        patternPassword = re.compile('^[a-zA-Z0-9]{8,}$')
        # print('Testing')
        # print(username, patternUsername.match(username))
        # print(email, patternEmail.match(email))
        # print(password, patternPassword.match(password))

        if (patternUsername.match(username) and
            patternEmail.match(email) and
            patternPassword.match(password) and
            (role.lower() == 'admin' or role.lower() == 'user' or role.lower() == 'member')):
            print('Validation correct.')
            return func(*args, **kwargs)

        else:
            # return jsonify({"Message" : "Validation Failed!"}),403 # return response
            print('Validaton failed.')
            return render_template('login.html', params=Param.RegisteringWithErrorParams()), 401

    return validate

# Validate Number
def validateNumber(num):
    pattern = '^\d+[.]?\d+$'
    reg = re.compile(pattern)
    num = str(num)
    if reg.match(num):
        return True
    else:
        return False

## Validate User Info b4 Update
def validateUpdate(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):

        # Creat Dictionary for List of Patterns
        patternUsername=re.compile('^[a-zA-Z0-9]+$')
        patternEmail=re.compile('^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$')
        patternPassword=re.compile('^[a-zA-Z0-9]{8,}$')

        dict_Pattern = {'username': patternUsername, \
                        'email' : patternEmail, \
                        'password': patternPassword, \
                        'role': ['admin', 'member', 'user'] }

        validate = True
        userJson = request.json
        if len(userJson) == 0:
            validate = False
        else:
            for k, v in userJson.items():
                if k =='role':  # Role
                    result = v.lower() in dict_Pattern['role']
                else:
                    result = dict_Pattern[k].match(v)
                if not result:  # False
                    validate = False
                    break

        if validate:
            print("Validation OK!")
            return func(*args, **kwargs)

        else:
            print('Validation Failed!')
            return jsonify({"Message":"Validation Failed!"}),403 #return response

    return validate 

def validatePassword(func):
    @functools.wraps(func)
    def validatepw(*args, **kwargs):
        password = request.form['passwordf']

        patternPassword = re.compile('^[a-zA-Z0-9]{8,}$')

        if (patternPassword.match(password)):
            print('Validation correct.')
            return func(*args, **kwargs)

        else:
            print('Validaton failed.')
            return render_template('login.html', params=Param.ForgotWithErrorParams()), 401

    return validatepw
