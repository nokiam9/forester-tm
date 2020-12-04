# -*- coding: utf-8 -*-
import os 

MONGODB_SETTINGS = {
    'db': 'cmccb2b',
    'username': 'root', #os.getenv('MONGODB_USERNAME'),
    'password': 'forester', #os.getenv('MONGODB_PASSWORD'),
    'host': 'forester-mongo', #os.getenv('MONGODB_HOST'),
    'port': 27017, #int(os.getenv('MONGODB_PORT')),
    'connect': False,  # set for pymongo bug fix
    'authentication_source': 'admin', # set authentication source database， default is MONGODB_NAME
     }

# SECRET_KEY = "flask+mongoengine=<3"     # flask-debug必须设置该参数，为session提供加密处理

# DEBUG_TB_INTERCEPT_REDIRECTS = False
