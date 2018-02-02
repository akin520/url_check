#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sys
import io
import beanstalkc
import subprocess
import threading
import multiprocessing.pool
import redis
import msgpack
import json
from influxdb import InfluxDBClient

from utils import config
from utils.logs import Logs
from utils.push import mail,sms

CONFIG = config.CONFIG
logger = Logs().logger

def connredis():
    client =redis.Redis(host=CONFIG['redis']['ip'], port=CONFIG['redis']['port'],db=0)
    return client

def connbeanstalk():
    beanstalk=beanstalkc.Connection(host=CONFIG['beanstalk']['ip'], port=CONFIG['beanstalk']['port'])
    return beanstalk


def conninfluxdb():
    client = InfluxDBClient(CONFIG['influxdb']['ip'], CONFIG['influxdb']['port'], CONFIG['influxdb']['user'], CONFIG['influxdb']['password'], CONFIG['influxdb']['database'])
    return client

def bsconsumer():
    print "bsconsumer start"
    logger.info("bsconsumer start")
    bsclient = connbeanstalk()
    bsclient.use('url_check')
    bsclient.watch('url_check')
    influxclient = conninfluxdb()
    influxclient.create_database('url_check')
    while True:
        try:
            job1=bsclient.reserve()
            json_data = msgpack.unpackb(job1.body)
            req = influxclient.write_points(json_data)
            if req:
                job1.delete()
        except Exception,e:
            logger.error('bsconsumer error %s ' % (str(e),))
            print(e)
            time.sleep(2)


def redisconsumer():
    print "redisconsumer start"
    logger.info("redisconsumer start")
    bsclient = connbeanstalk()
    bsclient.use('url_alarm')
    bsclient.watch('url_alarm')
    redisclient = connredis()
    while True:
        try:
            job1=bsclient.reserve()
            redis_value = msgpack.unpackb(job1.body)
            redis_key = "alarm" + ':' + str(int(time.time())/3600)
            #print redis_value
            if redisclient.hexists(redis_key,redis_value):
                redisclient.hincrby(redis_key,redis_value)
            else:
                redisclient.hset(redis_key,redis_value,1)
                redisclient.expire(redis_key, 3600+60)
            job1.delete()
        except Exception,e:
            print(e)
            time.sleep(2)



def minute_alarm(step):
    client = connredis()
    while True:
        now = int(time.time())
        redis_key = "alarm" + ':' + str(int(time.time())/3600)
        minute_key = "minute" + ':' + str(int(time.time())/3600)
        hashall = client.hgetall(redis_key)
        if hashall.keys():
            print "[ %s ] ms to print1 %s " % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),str(hashall.keys()))
            logger.info("print 1 %s" % (str(hashall.keys())))
            for i,j in hashall.items():
                if int(j) > CONFIG['count']:
                    logger.info("print 1 gt %d %s" % (CONFIG['count'],str(hashall.keys())))
                    if client.hexists(minute_key,i):
                        times = int(client.hget(minute_key,i))
                        if times < CONFIG['times']:
                            print("print 1 gt %d %s" % (times,i))
                            msg = {}
                            msg['content'] = str(i)
                            json_data = json.dumps(msg)
                            sms(json_data)
                            client.hset(redis_key,i,1)
                        else:
                            print("print 1 gt %d %s" % (times,i))
                            logger.info("print 1 gt %d %s" % (times,i))
                        client.hincrby(minute_key,i)
                    else:
                        msg = {}
                        msg['content'] = str(i)
                        json_data = json.dumps(msg)
                        sms(json_data)
                        client.hset(minute_key,i,1)
                        client.expire(minute_key, 3600+60)
                        client.hset(redis_key,i,1)
        dlt = time.time() - now
        if dlt < step:
            time.sleep(step - dlt)
    

if __name__ == '__main__':
    logger.info("CONFIG : %s" % CONFIG)
    t0 = threading.Thread(target=bsconsumer)
    t0.daemon = False
    t0.start()
    t1 = threading.Thread(target=redisconsumer)
    t1.daemon = False
    t1.start()
    t2 = threading.Thread(target=minute_alarm, args=(300,))
    t2.daemon = False
    t2.start()