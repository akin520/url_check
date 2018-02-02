#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class Items(models.Model):
    host = models.CharField(max_length=100,verbose_name=u"节点")
    region = models.CharField(max_length=100,verbose_name=u"区域",blank=True, null=True)
    url = models.CharField(max_length=100,verbose_name=u"URL连接")
    http_code = models.IntegerField(verbose_name=u"状态",blank=True, null=True)
    namelookup_time = models.DecimalField(max_digits=19,decimal_places=10,verbose_name=u"DNS解析域名",blank=True, null=True)
    connect_time = models.DecimalField(max_digits=19,decimal_places=10,verbose_name=u"建立TCP连接",blank=True, null=True)
    pertransfer_time = models.DecimalField(max_digits=19,decimal_places=10,verbose_name=u"第一个远程请求接收到第一个字节",blank=True, null=True)
    starttransfer_time = models.DecimalField(max_digits=19,decimal_places=10,verbose_name=u"响应第一个字节返回",blank=True, null=True)
    total_time = models.DecimalField(max_digits=19,decimal_places=10,verbose_name=u"发送会所有的相应数据",blank=True, null=True)
    size_download = models.IntegerField(verbose_name=u"文件大小",blank=True, null=True)
    head_size = models.IntegerField(verbose_name=u"头部大小",blank=True, null=True)
    speed_download = models.IntegerField(verbose_name=u"下载速度",blank=True, null=True)
    add_date = models.DateTimeField(verbose_name=u"添加时间", auto_now_add=True)
    #add_date = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'items'
        verbose_name = u"详情管理"
        verbose_name_plural = verbose_name



