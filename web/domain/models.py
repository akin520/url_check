#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

STATUS = (
    (0, u"不回源"),
    (1, u"回源"),
)

ENABLE = (
    (0, u"不采集"),
    (1, u"采集"),
)

class Domain(models.Model):
    name = models.CharField(max_length=100,verbose_name=u"域名")
    url = models.CharField(max_length=100,verbose_name=u"URL连接")
    status = models.SmallIntegerField(choices=STATUS, verbose_name=u"是否回源", default=0)
    proxy = models.CharField(max_length=100,verbose_name=u"回源地址",blank=True, null=True)
    enable = models.SmallIntegerField(choices=ENABLE, verbose_name=u"是否采集", default=1)
    add_date = models.DateTimeField(verbose_name=u"添加时间", auto_now = True)
    update_date = models.DateTimeField(verbose_name=u"更新时间", auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'domain'
        verbose_name = u"域名管理"
        verbose_name_plural = verbose_name

