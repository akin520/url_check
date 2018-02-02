#!/usr/bin/env python
#coding:utf-8

import json
import time
import pycurl
import io


def curl_url(url,SERVER,REGION,NAME,CONNECTTIMEOUT,TIMEOUT,TIME):
    h = io.BytesIO()
    b = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.HEADERFUNCTION, h.write)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.ENCODING, 'gzip')
    c.setopt(pycurl.CONNECTTIMEOUT, CONNECTTIMEOUT) #链接超时
    c.setopt(pycurl.TIMEOUT, TIMEOUT)  #下载超时
    c.setopt(pycurl.USERAGENT, "FH21_URL_CHECK v0.01") #模拟浏览器
    c.setopt(pycurl.FOLLOWLOCATION, 1) #允许跳转
    c.setopt(pycurl.URL,url)
    try:
        c.perform()
    except Exception,e:
        print(e)
    NAMELOOKUP_TIME =  c.getinfo(c.NAMELOOKUP_TIME)
    CONNECT_TIME =  c.getinfo(c.CONNECT_TIME)
    PRETRANSFER_TIME =   c.getinfo(c.PRETRANSFER_TIME)
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
    HTTP_CODE =  c.getinfo(c.HTTP_CODE)
    SIZE_DOWNLOAD =  c.getinfo(c.SIZE_DOWNLOAD)
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
    SPEED_DOWNLOAD=c.getinfo(c.SPEED_DOWNLOAD)
    json_body = [
    {
        "measurement": "url_check",
        "tags": {
            "host": SERVER,
            "region": REGION,
            "url":url,
            "code":HTTP_CODE,
            "name":NAME
        },
        "time": TIME,
        "fields": {
            "http_code": HTTP_CODE,
            "namelookup_time": NAMELOOKUP_TIME,
            "connect_time": CONNECT_TIME,
            "pertransfer_time": PRETRANSFER_TIME,
            "starttransfer_time": STARTTRANSFER_TIME,
            "total_time": TOTAL_TIME,
            "size_download": SIZE_DOWNLOAD,
            "head_size": HEADER_SIZE,
            "speed_download": SPEED_DOWNLOAD
        }
    },
    ]
    return json_body

def curl_proxy(url,SERVER,REGION,NAME,PROXY,CONNECTTIMEOUT,TIMEOUT,TIME):
    h = io.BytesIO()
    b = io.BytesIO()
    proxy = "http://" + str(PROXY)+":80"
    c = pycurl.Curl()
    c.setopt(pycurl.HEADERFUNCTION, h.write)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.ENCODING, 'gzip')
    c.setopt(pycurl.CONNECTTIMEOUT, CONNECTTIMEOUT) #链接超时
    c.setopt(pycurl.TIMEOUT, TIMEOUT)  #下载超时
    c.setopt(pycurl.PROXY, proxy)#设置代理
    #c.setopt(pycurl.PROXYUSERPWD, 'aaa:aaa')
    c.setopt(pycurl.USERAGENT, "FH21_URL_CHECK v0.01") #模拟浏览器
    c.setopt(pycurl.FOLLOWLOCATION, 1) #允许跳转
    c.setopt(pycurl.URL,url)
    try:
        c.perform()
    except Exception,e:
        print(e)
    NAMELOOKUP_TIME =  c.getinfo(c.NAMELOOKUP_TIME)
    CONNECT_TIME =  c.getinfo(c.CONNECT_TIME)
    PRETRANSFER_TIME =   c.getinfo(c.PRETRANSFER_TIME)
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
    HTTP_CODE =  c.getinfo(c.HTTP_CODE)
    SIZE_DOWNLOAD =  c.getinfo(c.SIZE_DOWNLOAD)
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
    SPEED_DOWNLOAD=c.getinfo(c.SPEED_DOWNLOAD)
    json_body = [
    {
        "measurement": "url_check",
        "tags": {
            "host": SERVER,
            "region": REGION,
            "url":url,
            "code":HTTP_CODE,
            "name":NAME
        },
        "time": TIME,
        "fields": {
            "http_code": HTTP_CODE,
            "namelookup_time": NAMELOOKUP_TIME,
            "connect_time": CONNECT_TIME,
            "pertransfer_time": PRETRANSFER_TIME,
            "starttransfer_time": STARTTRANSFER_TIME,
            "total_time": TOTAL_TIME,
            "size_download": SIZE_DOWNLOAD,
            "head_size": HEADER_SIZE,
            "speed_download": SPEED_DOWNLOAD
        }
    },
    ]
    return json_body
