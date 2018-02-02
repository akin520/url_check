#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class Alarm(models.Model):
    name = models.CharField(max_length=100,verbose_name=u"名称")
    url = models.CharField(max_length=100,verbose_name=u"URL连接")
    node = models.CharField(max_length=100,verbose_name=u"节点")
    status = models.IntegerField(verbose_name=u"状态", blank=True, null=True)
    add_date = models.DateTimeField(default=timezone.now, verbose_name=u"添加时间")

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'alarm'
        verbose_name = u"报警管理"
        verbose_name_plural = verbose_name



