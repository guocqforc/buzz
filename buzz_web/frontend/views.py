# coding: utf8

from collections import defaultdict
from django.shortcuts import render
from share.utils import jsonify

from share.models import Config


def load_config(request):
    """
    从数据库拉取配置
    :param request:
    :return:
    """

    json_config = list()

    for conf in Config.objects.all():
        json_config.append(dict(
            id=conf.id,
            stat_name=conf.stat_name,
            number_op=conf.number_op,
            number_value=conf.number_value,
            slope_op=conf.slope_op,
            slope_value=conf.slope_value,
        ))

    return jsonify(
        ret=0,
        config=json_config,
    )
