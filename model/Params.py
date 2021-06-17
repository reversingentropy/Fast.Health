# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 20:35:00 2021

@author: Lenovo
"""

class Param:

    param = {}
    param['loggingIn'] = False
    param['registering'] = False
    param['forgotpass'] = False
    param['displayMesg'] = False
    param['displayMesgr'] = False
    param['displayMesgf'] = False
    param['changeButton'] = False
    param['deleteButton'] = False

    @classmethod
    def SetAllFalseParams(cls):
        cls.param['loggingIn'] = False
        cls.param['registering'] = False
        cls.param['forgotpass'] = False
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = False
        return cls.param

    @classmethod
    def LoggingNoErrorParams(cls):
        cls.param['loggingIn'] = True
        cls.param['registering'] = False
        cls.param['forgotpass'] = False
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = False
        return cls.param

    @classmethod
    def LoggingWithErrorParams(cls):
        cls.param['loggingIn'] = True
        cls.param['registering'] = False
        cls.param['forgotpass'] = False
        cls.param['displayMesg'] = True
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = False
        return cls.param

    @classmethod
    def RegisteringNoErrorParams(cls):
        cls.param['loggingIn'] = False
        cls.param['registering'] = True
        cls.param['forgotpass'] = False
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = False
        return cls.param
        
    @classmethod
    def RegisteringWithErrorParams(cls):
        cls.param['loggingIn'] = False
        cls.param['registering'] = True
        cls.param['forgotpass'] = False
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = True
        cls.param['displayMesgf'] = False
        return cls.param
        
    @classmethod
    def ForgotNoErrorParams(cls):
        cls.param['loggingIn'] = False
        cls.param['registering'] = False
        cls.param['forgotpass'] = True
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = False
        return cls.param

    @classmethod
    def ForgotWithErrorParams(cls):
        cls.param['loggingIn'] = False
        cls.param['registering'] = False
        cls.param['forgotpass'] = True
        cls.param['displayMesg'] = False
        cls.param['displayMesgr'] = False
        cls.param['displayMesgf'] = True
        return cls.param

    @classmethod
    def UserTableNoButtons(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = False
        return cls.param

    @classmethod
    def UserTableChangeButton(cls):
        cls.param['changeButton'] = True
        cls.param['deleteButton'] = False
        return cls.param

    @classmethod
    def UserTableDeleteButton(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = True
        return cls.param

    @classmethod
    def PatientsTableDefButton(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = False
        cls.param['queryButton'] = True
        return cls.param

    @classmethod
    def PatientsTableUpdateButton(cls):
        cls.param['changeButton'] = True
        cls.param['deleteButton'] = False
        cls.param['queryButton'] = False
        return cls.param

    @classmethod
    def PatientsTableDeleteButton(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = True
        cls.param['queryButton'] = False
        return cls.param
       
    @classmethod
    def QueryTableNoButtons(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = False
        return cls.param

    @classmethod
    def QueryTableUpdateButton(cls):
        cls.param['changeButton'] = True
        cls.param['deleteButton'] = False
        return cls.param

    @classmethod
    def QueryTableDeleteButton(cls):
        cls.param['changeButton'] = False
        cls.param['deleteButton'] = True
        return cls.param
