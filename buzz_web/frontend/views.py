# coding: utf8

from django.shortcuts import render
from share.utils import jsonify


def load_config(request):
    """
    从数据库拉取配置
    :param request:
    :return:
    """

    return jsonify(
        ret=0
    )
