# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from . import json_extend


def jsonify(*args, **kwargs):
    """支持时间、日期的jsonify"""
    encoded_data = json.dumps(
        dict(*args, **kwargs),
        ensure_ascii=False,
        cls=json_extend.DatetimeJSONEncoder,
        )

    return HttpResponse(
        encoded_data,
        content_type='application/json'
        )
