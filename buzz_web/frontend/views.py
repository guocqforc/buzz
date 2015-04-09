# coding: utf8

import json
import hashlib
import logging
from collections import defaultdict
from django.shortcuts import render
from share.utils import jsonify
from share.models import Config, Person, Role, Alarm
from django.conf import settings
from share.utils import send_mail

logger = logging.getLogger('django.request')


def load_config(request):
    """
    从数据库拉取配置
    """

    json_config = list()

    for conf in Config.objects.all():
        if not conf.valid:
            continue

        json_config.append(dict(
            id=conf.id,
            stat_name=conf.stat_name,
            number_cmp=conf.number_cmp,
            number_value=conf.number_value,
            slope_cmp=conf.slope_cmp,
            slope_value=conf.slope_value,
        ))

    return jsonify(
        ret=0,
        config=json_config,
    )


def send_alarm(request):
    """
    发送警报
    """
    data = request.REQUEST.get('data')
    sign = request.REQUEST.get('sign')

    if not data or not sign:
        return jsonify(
            ret=-1,
            error=u'参数错误',
        )

    calc_sign = hashlib.md5('|'.join([settings.ALARM_SECRET, data])).hexdigest()
    if calc_sign != sign:
        return jsonify(
            ret=-2,
            error=u'签名错误'
        )

    json_data = json.loads(data)

    try:
        config = Config.objects.get(pk=json_data['config_id'])
    except Config.DoesNotExist:
        return jsonify(
            ret=-3,
            error=u'config不存在'
        )
    except:
        logger.error('exc occur.', exc_info=True)
        return jsonify(
            ret=-4,
            error=u'未知错误'
        )

    alarm = Alarm()
    alarm.config = config
    alarm.number_value = json_data['number_value']
    alarm.slope_value = json_data['slope_value']
    alarm.notified = False
    # 先保存起来，说明还没有邮件通知
    alarm.save()

    receivers = set()

    for role in config.roles.all():
        for person in role.person_set.all():
            receivers.add(person.email)

    for person in config.persons.all():
        receivers.add(person.email)

    content = u'统计项: %s\n' % config.stat_name

    if json_data['number_value'] is not None:
        # 说明是相关的
        content += u'值类型: %s %s %s\n' % (json_data['number_value'], config.number_cmp, config.number_value)

    if json_data['slope_value'] is not None:
        # 说明是相关的
        content += u'波动率: %.02f %s %.02f\n' % (json_data['slope_value'], config.slope_cmp, config.slope_value)

    logger.error('data: %s, content: %s', data, content)

    try:
        send_mail(receivers, settings.MAIL_SUBJECT, content)
    except:
        logger.error('exc occur.', exc_info=True)
        return jsonify(
            ret=-5,
            error=u'发送邮件异常'
        )

    # 发送成功
    alarm.notified = True
    alarm.save()

    return jsonify(
        ret=0
    )
