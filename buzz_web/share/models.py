# coding: utf8
import datetime
from django.db import models
from django.conf import settings


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name=u'昵称', max_length=255)
    intro = models.TextField(verbose_name=u'介绍', null=True, blank=True)

    class Meta:
        verbose_name = u'角色'


class Person(models.Model):
    """
    操作用户
    """
    name = models.CharField(verbose_name=u'昵称', max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name=u'邮箱')
    phone = models.CharField(verbose_name=u'电话', max_length=255, null=True, blank=True)
    roles = models.ManyToManyField(Role, verbose_name=u'角色列表')

    def __unicode__(self):
        return u'%s' % self.nick

    class Meta:
        verbose_name = u'负责人'


class Config(models.Model):
    """
    配置
    """
    stat_name = models.CharField(verbose_name=u'统计项名称', max_length=255)

    number_op = models.CharField(verbose_name=u'值类型操作',
                                 max_length=255, choices=settings.OP_CHOICES, null=True, blank=True)
    number_value = models.IntegerField(verbose_name=u'值类型数值', null=True, blank=True)

    slope_op = models.CharField(verbose_name=u'斜率类型操作',
                                max_length=255, choices=settings.OP_CHOICES, null=True, blank=True)
    slope_value = models.FloatField(verbose_name=u'斜率类型数值', null=True, blank=True)

    notify_roles = models.ManyToManyField(Role, verbose_name=u'告警组', null=True, blank=True)
    notify_persons = models.ManyToManyField(Person, verbose_name=u'告警人', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.stat_name

    class Meta:
        verbose_name = u'报警配置'


class Alarm(models.Model):
    """
    报警
    """

    stat_name = models.CharField(verbose_name=u'统计项名称', max_length=255)
    create_time = models.DateTimeField(verbose_name=u'报警时间', default=datetime.datetime.now)
    number_value = models.IntegerField(verbose_name=u'值类型数值', null=True, blank=True)
    slope_value = models.FloatField(verbose_name=u'斜率类型数值')
    notified = models.BooleanField(verbose_name=u'通知成功')

    def __unicode__(self):
        return u'%s-%s' % (self.stat_name, self.create_time)

    class Meta:
        verbose_name = u'报警历史'
