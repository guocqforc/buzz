# coding: utf8

import json
import hashlib
import logging
from collections import defaultdict
from django.shortcuts import render
from share.utils import jsonify
from share.models import Config
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

    return jsonify(
        ret=0
    )
