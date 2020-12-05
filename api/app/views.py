# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from mongoengine.errors import NotUniqueError

from models import BidNoticeModel

import json
import datetime

class Notice(Resource):
    def get(self, nid):
        x = BidNoticeModel.objects.filter(nid=nid).first()  # pylint: disable=no-member
        if (x):
            return x.to_json(), 200
        else :
            return 'no rec', 200
    
    def post(self, nid):        # insert a new item
        # data = 
        json_data = json.loads(request.get_data().decode("utf-8"))
        # print(json_data)
        try:
            BidNoticeModel(
                title = json_data['title'], 
                nid = json_data['nid'],
                notice_type = json_data['notice_type'],
                type_id = json_data['type_id'], 
                spider = json_data['spider'], 
                source_ch = json_data['source_ch'],
                notice_url = json_data['notice_url'],
                notice_content = json_data['notice_content'], 
                # TM POST为页面原始格式，API网关负责Date格式转换
                published_date = datetime.datetime.strptime(json_data['published_date'], '%Y-%m-%d'),
                # 时间戳取自API网关的当前时间
                timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=8),
                # reminded_time = null, 
                # attachment_urls = null
                # attachment_files = null
            ).save()
        except (NotUniqueError):  ## DuplicateKeyError,
            print('Dup rec! nid=' + json_data['nid'])
            return 'dup rec', 200
        except ValueError as e:
            print('Unknown error:', e)
            return('error',200)

        return 'post ok', 200          # 204 when duplicate

    def delete(self, nid):      # delete item is not supported
        return '', 403

    def put(self, nid):         # update item is not supported  
        return '', 403

# NoticeList
#   shows a list of all items
class NoticeList(Resource):
    def get(self):              # list all item
        return 'pass',200


# Content
#   get and post contend of a notice
class Content(Resource):
    def get(self, nid):
        x = BidNoticeModel.objects.filter(nid=nid).first()  # pylint: disable=no-member
        if (x):
            return x.notice_content, 200
        else :
            return 'no rec', 200
    
    def post(self, Resource):
        pass 
        return '', 200

class Hello(Resource):
    def get(self):
        return "Hello API of forester!"