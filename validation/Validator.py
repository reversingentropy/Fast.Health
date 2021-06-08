import functools
from flask import Flask,jsonify,request,g, redirect, make_response, render_template
from config.settings import Settings

import jwt
import re



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


## Validate User Info b4 Insert
def validateRegister(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        username=request.json['username']
        email=request.json['email']
        role=request.json['role']
        password=request.json['password']

        patternUsername=re.compile('^[a-zA-Z0-9]+$')

        #simple email check
        #patternEmail=re.compile('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+@\w+\.\w+$') 
        patternEmail=re.compile('^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$')
        patternPassword=re.compile('^[a-zA-Z0-9]{8,}$')

        if(patternUsername.match(username) and patternEmail.match(email) and patternPassword.match(password) ):
            print("Validation OK!")
            return func(*args, **kwargs)

        else:
            print('Validation Failed!')
            return jsonify({"Message":"Validation Failed!"}),403 #return response

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
