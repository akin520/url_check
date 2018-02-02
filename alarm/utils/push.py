#!/usr/bin/env python
#coding:utf-8
import json
import urllib2

from utils import config
from utils.logs import Logs

CONFIG = config.CONFIG
logger = Logs().logger


def mail(values):
    try:
        req = urllib2.Request(CONFIG['push']['mail'],values)   #生成页面请求的完整数据
        response = urllib2.urlopen(req)    # 发送页面请求
    except urllib2.HTTPError,error:
        logger.error("ERROR: %s" % error.read())

def sms(values):
    try:
        req = urllib2.Request(CONFIG['push']['sms'],values)   #生成页面请求的完整数据
        response = urllib2.urlopen(req)    # 发送页面请求
    except urllib2.HTTPError,error:
        logger.error("ERROR: %s" % error.read())
