#!/usr/bin/env python
#coding:utf-8

import sys
import os
import django
import json
import msgpackrpc
import beanstalkc
import redis
import msgpack

from utils import config
from utils.logs import Logs

CONFIG = config.CONFIG
logger = Logs().logger

def connbeanstalk():
    beanstalk=beanstalkc.Connection(host=CONFIG['beanstalk']['ip'],port=CONFIG['beanstalk']['port'])
    return beanstalk

def redis_conn():
    client =redis.Redis(host=CONFIG['redis']['ip'],port=CONFIG['redis']['port'],db=0)
    return client

#配置使用django
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print BASE_DIR
#sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'url_check.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_check.settings")
django.setup()


#使用django orm
#from domain.models import Domain
#all = Domain.objects.all()
#from django.core import serializers
#json1 = serializers.serialize("json", all)
#print json1,type(json.loads(json1))
#for i in json.loads(json1):
#   print i['fields']['url'],i['fields']['status'],i['fields']['proxy']

            
from domain.models import Domain
from django.core import serializers


class RpcServer(object):
    def getalldomain(self):
        redis_client = redis_conn()
        if redis_client.exists('getall'):
            json1 = redis_client.get('getall')
        else:
            getall = Domain.objects.all().filter(enable=1)
            #getall = Domain.objects.all()
            logger.info("getall: %d",len(getall))
            json1 = serializers.serialize("yaml", getall)
            redis_client.set('getall',json1)
            #logger.info("json: %s", json1)
            redis_client.expire('getall',3600)
        return json1

    def push_metrics(self,x):
        bs = connbeanstalk()
        bs.use('url_check')
        bs.put(x)
        return 1

    def push_alarm(self,x):
        bs = connbeanstalk()
        bs.use('url_alarm')
        bs.put(x)
        return 1

server = msgpackrpc.Server(RpcServer())
server.listen(msgpackrpc.Address("0.0.0.0", CONFIG['listen']))
server.start()


