# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from mongoengine.errors import NotUniqueError

from models import BidNoticeModel

import json
import datetime


def notice2dict(cls):
    return {
        'title': cls.title,
        'nid': cls.nid,
        'notice_type': cls.notice_type,
        'type_id': cls.type_id,
        'spider': cls.spider,
        'source_ch': cls.source_ch,
        'published_date': cls.published_date.strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp': cls.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        # 'notice_url': std.notice_url,
        # 'notice_content': std.notice_content
    }
# pylint: disable=no-member
class Notice(Resource):
    def get(self, nid):
        rec = BidNoticeModel.objects.filter(nid=nid).first()  
        if (rec):
            return json.dumps(rec, default=notice2dict), 200
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

# Page
#   shows a page of all items, 
#   URL: /v1/notice?type_id=2&page_id=0&page_size=10
class Page(Resource):
    def get(self):              # list all item
        type_id = request.args.get('type_id', default='0', type=str)
        page_id = request.args.get('page_id', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        if type_id == '0' :
            records = BidNoticeModel.objects(). \
                order_by("-published_date", "-timestamp"). \
                paginate(page=page_id, per_page=page_size)
        else:
            records = BidNoticeModel.objects(type_id=type_id). \
                order_by("-published_date", "-timestamp"). \
                paginate(page=page_id, per_page=page_size)
        if (records):
            return json.dumps(records.items, default=notice2dict), 200
        else :
            return 'no rec', 200
    
    def post(self):
        pass
        return 'error', 200
    
    def delete(self):
        return '', 403
    
    def put(self):
        return '', 403


# Content
#   get and post contend of a notice
class Content(Resource):
    def get(self, nid):
        # pylint: disable=no-member
        x = BidNoticeModel.objects.filter(nid=nid).first()  
        if (x):
            return x.notice_content, 200
        else :
            return 'no rec', 200
    
    def post(self, Resource):
        pass 
        return '', 200

class Hello(Resource):
    def get(self):
        return "Hi! Here is open api gateway of forester."