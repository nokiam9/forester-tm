from typing import ContextManager
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

# 初始化app，原型在flask，并从settings.py中提取自定义的类属性，包括MongoDB配置，debug配置等
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_pyfile(filename='settings.py')
api = Api(app)

NOTICE_TYPE_CONFIG = {
    '0': '全部招标公告',
    '1': '单一来源采购公告',
    '2': '采购公告',
    '7': '中标结果公示',
    '3': '资格预审公告',
    '8': '供应商信息收集',
    '99': '供应商公告',
}

PAGE_SIZE = 10

NOTICES = {
    'nid1': {'task': 'build an API'},
    'nid2': {'task': '?????'},
    'nid3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(nid):
    if nid not in NOTICES:
        abort(404, message="NOTICES{} doesn't exist".format(nid))

parser = reqparse.RequestParser()
parser.add_argument('nid', type=str)
parser.add_argument('title', type=str)

# Notice
#   show or insert a single item 
class Notice(Resource):
    def get(self, nid):
        abort_if_todo_doesnt_exist(nid)
        # return NOTICES[nid]
        return 'get ok', 200
    
    def post(self, nid):        # insert a new item
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        print(args)
        pass 
        return 'post ok', 200          # 204 when duplicate

    def delete(self, nid):      # delete item is not supported
        return '', 403

    def put(self, nid):         # update item is not supported  
        return '', 403

# NoticeList
#   shows a list of all items
class NoticeList(Resource):
    def get(self):              # list all item
        return NOTICES


# Content
#   get and post contend of a notice
class Content(Resource):
    def get(self, nid):
        pass
        return '', 200
    
    def post(Resource):
        pass 
        return '', 200

##
## Actually setup the Api resource routing here
##
api.add_resource(NoticeList, '/v1/notice')
api.add_resource(Notice, '/v1/notice/<string:nid>')
api.add_resource(Content, '/v1/notice/<string:nid>/content')
# api.add_resource('/notice/pagination/<string:type_id>', view_func=views.notice_page_view)


if __name__ == "__main__":

    # app.run()启动flask自带web server
    # 嵌入uWSGI后app.run()不会执行，而是引用该py的app变量，uWSGI的设置在uwsgi.ini中，port也会修改
    app.run(host='0.0.0.0', debug=False, port=3000)
