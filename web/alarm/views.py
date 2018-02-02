#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json,yaml
import base64

#import sendmail
#import sendsms

def index(request):
    if request.method == "POST":
        print request.body
        return HttpResponse("hi")
    else:
        return HttpResponse("hello world")

def mail(request):
    data = request.body
    req = json.loads(data)
    #req = yaml.safe_load(req)
    text = base64.b64decode(req['content'])
    post = text.split("||")
    print post
    """
    实现mail发送
    """
    return HttpResponse("mail")

def sms(request):
    data = request.body
    req = json.loads(data)
    #req = yaml.safe_load(req)
    text = base64.b64decode(req['content'])
    post = text.split("||")
    print post
    """
    实现sms发送
    """
    return HttpResponse("sms")

