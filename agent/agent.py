#!/usr/bin/env python
#coding:utf-8

import os
import time
import sys
import subprocess
import threading
import multiprocessing.pool
import msgpackrpc
import msgpack
import yaml
import base64

from utils import config
from utils.logs import Logs
from utils.url import curl_url,curl_proxy

CONFIG = config.CONFIG
logger = Logs().logger

def connrpcserver():
    client = msgpackrpc.Client(msgpackrpc.Address(CONFIG['rpcserver']['ip'], CONFIG['rpcserver']['port']))
    return client

def url_check(step,urls):
    load_num = 0
    process_count = CONFIG['process']
    server = CONFIG['server']
    region = CONFIG['region']
    timeout = CONFIG['timeout']
    connecttimeout = CONFIG['connecttimeout']
    client = connrpcserver()
    logger.info("multiprocess count is : %s" % process_count)
    while True:
        #refresh urls
        load_num += 1
        logger.info("load_num is : %s" % load_num)
        if load_num == (2*process_count):
            load_num = 0
            client = connrpcserver()
            getall = client.call('getalldomain')
            urls = list(yaml.load_all(getall))[0]
            logger.info("refresh urls")
            logger.info("URLS : %d" % len(urls))    
            
        pool = multiprocessing.Pool(process_count)
        now = int(time.time())
        metrics = []
        result = []
        for url in urls:
            if url["fields"]["status"]:
                result.append(pool.apply_async(curl_proxy, (url['fields']['url'],server,region,url['fields']['name'],url['fields']['proxy'],connecttimeout,timeout,time.strftime("%Y-%m-%d %X", time.gmtime(now)))))
            else:
                result.append(pool.apply_async(curl_url, (url['fields']['url'],server,region,url['fields']['name'],connecttimeout,timeout,time.strftime("%Y-%m-%d %X", time.gmtime(now)))))
        pool.close()
        pool.join()

        for res in result:
            metrics.extend(res.get())

        print metrics,type(metrics),len(metrics)
        try:
            req = client.call('push_metrics',msgpack.packb(metrics))
            logger.info("push_metrics is : %s" % str(req))
        except Exception,e:
            logger.error("push_metrics is error : %s" % str(e))
            client = connrpcserver()
            req = client.call('push_metrics',msgpack.packb(metrics))
            logger.info("2 push_metrics is : %s" % str(req))
        
        #alarm code > 400 error
        for i in metrics:
            if int(i['fields']['http_code']) > 400 or (int(i['fields']['http_code']) < 200 and (int(i['fields']['http_code']) != 0)):
                value = u"{}||{}||{}||{}".format(i['tags']['name'],i['tags']['url'],i['tags']['host'],i['fields']['http_code'])
                y_d = yaml.dump(value)
                b_b = base64.b64encode(y_d)
                logger.error("alarm is %s" % value)
                try:
                    client.call('push_alarm',msgpack.packb(b_b))
                except Exception,e:
                    logger.error("push_alarm is error : %s" % str(e))
                    client = connrpcserver()
                    client.call('push_alarm',msgpack.packb(b_b))

        dlt = time.time() - now
        if dlt < step:
            time.sleep(step - dlt)
    

if __name__ == '__main__':
    client = connrpcserver()
    getall = client.call('getalldomain')
    urls = list(yaml.load_all(getall))[0]
    logger.info("CONFIG : %s" % CONFIG)    
    logger.info("URLS : %d" % len(urls))    
    t = threading.Thread(target=url_check, args=(60,urls))
    t.daemon = False
    t.start()
