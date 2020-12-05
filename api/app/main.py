# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from models import db
from views import Page, Notice, Content, Hello

import logging

# 初始化app，原型在flask，并从settings.py中提取自定义的类属性，包括MongoDB配置，debug配置等
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_pyfile(filename='settings.py')
api = Api(app)

# 连接flask和mongoengine，注意Table定义在models.py，DB参数设置已经从app.config中加载
db.init_app(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(Hello, '/')
# URL: /v1/notice?type_id=2&page_id=0&page_size=10
api.add_resource(Page, '/v1/notice')
# URL: /v1/notice/170348
api.add_resource(Notice, '/v1/notice/<string:nid>')
# URL: /v1/notice/170348/content
api.add_resource(Content, '/v1/notice/<string:nid>/content')



# api.add_resource('/notice/pagination/<string:type_id>', view_func=views.notice_page_view)

if __name__ == "__main__":
    # app.run()启动flask自带web server
    # 嵌入uWSGI后app.run()不会执行，而是引用该py的app变量，uWSGI的设置在uwsgi.ini中，port也会修改
    app.run(host='0.0.0.0', debug=False, port=3000)
