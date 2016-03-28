# coding: utf8
import datetime
from django.db import models
from django.conf import settings


class Role(models.Model):
    """
    角色，对应的是flylog的角色名称
    """
    name = models.CharField(verbose_name=u'名称', max_length=255)
    flylog_name = models.CharField(verbose_name=u'flylog名称', max_length=255)

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.flylog_name)

    class Meta:
        verbose_name = u'角色'


class Config(models.Model):
    """
    配置
    """
    stat_name = models.CharField(verbose_name=u'统计项', max_length=255)

    number_cmp = models.CharField(verbose_name=u'值类型比较符',
                                  max_length=255, choices=settings.OP_CHOICES, null=True, blank=True)
    number_value = models.FloatField(verbose_name=u'值类型数值', null=True, blank=True)

    slope_cmp = models.CharField(verbose_name=u'波动率比较符',
                                 max_length=255, choices=settings.OP_CHOICES, null=True, blank=True)
    slope_value = models.FloatField(verbose_name=u'波动率数值', null=True, blank=True)

    roles = models.ManyToManyField(Role, verbose_name=u'告警组', null=True, blank=True)

    valid = models.BooleanField(verbose_name=u'有效', default=True)

    def __unicode__(self):
        return u'%s' % self.stat_name

    class Meta:
        verbose_name = u'报警配置'


class Alarm(models.Model):
    """
    报警
    """

    config = models.ForeignKey(Config, verbose_name=u'告警配置')
    create_time = models.DateTimeField(verbose_name=u'报警时间', default=datetime.datetime.now)
    number_value = models.FloatField(verbose_name=u'值类型数值', null=True, blank=True)
    slope_value = models.FloatField(verbose_name=u'波动率数值', null=True, blank=True)
    notified = models.BooleanField(verbose_name=u'通知成功')

    def __unicode__(self):
        return u'%s-%s' % (self.config, self.create_time)

    class Meta:
        verbose_name = u'报警历史'
