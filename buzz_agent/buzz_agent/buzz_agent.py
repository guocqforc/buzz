# -*- coding: utf-8 -*-

import json
import datetime
import urlparse
import logging
import os.path
import hashlib
import requests
import whisper

logger = logging.getLogger('default')


LOAD_CONFIG_PATH = '/config'
ALARM_PATH = '/alarm'


class BuzzAgent(object):

    path = None
    domain = None
    secret = None
    interval = None

    last_run_time = None
    alarm_config = None

    def __init__(self, path, domain, secret, interval):
        self.path = path
        self.domain = domain
        self.secret = secret
        self.interval = interval

    def run(self):
        if not self.last_run_time:
            self.last_run_time = datetime.datetime.now() - datetime.timedelta(seconds=self.interval)

        if not self._load_config():
            if not self.alarm_config:
                # 只有没有配置的情况下才报错
                return False

        now = datetime.datetime.now()

        for conf in self.alarm_config:
            stat_path = os.path.join(self.path, conf['stat_name'].replace('.', '/'))
            logger.debug('stat_path: %s', stat_path)

            try:
                values = self._fetch_stat_data(stat_path, self.last_run_time, now)
            except:
                logger.error('exc occur. stat_path: %s, conf: %s', stat_path, conf, exc_info=True)
                continue

            for k, v in enumerate(values):
                alarm_benchmark = 0
                alarm_num = 0

                number_value = v
                slope_value = None

                if conf['number_op'] is not None and conf['number_value'] is not None:
                    # 值

                    alarm_benchmark += 1
                    code = '%s %s %s' % (number_value, conf['number_op'], conf['number_value'])
                    if eval(code):
                        alarm_num += 1

                if conf['slope_op'] is not None and conf['slope_value'] is not None:
                    # 斜率

                    alarm_benchmark += 1

                    if k > 0:
                        # 说明可以计算斜率
                        pre_val = values[k-1]

                        if pre_val > 0:
                            slope_value = (v - pre_val) / pre_val
                        else:
                            slope_value = None

                        if slope_value is not None:
                            code = '%s %s %s' % (slope_value, conf['slope_op'], conf['slope_value'])
                            if eval(code):
                                alarm_num += 1

                if alarm_benchmark and alarm_benchmark == alarm_num:
                    # 说明要告警

                    self._alarm(conf['id'], number_value, slope_value)

    def _fetch_stat_data(self, stat_path, from_time, to_time):
        """
        获取数据
        :return:
        """
        time_info, values = whisper.fetch(stat_path, from_time, to_time)

        return values

    def _load_config(self):
        """
        读取配置
        :return:
        """

        url = urlparse.urljoin('http://' + self.domain, LOAD_CONFIG_PATH)

        rsp = requests.get(url)
        if not rsp.ok:
            logger.error('fail. url: %s', url)
            return False

        self.alarm_config = rsp.json()

        return True

    def _alarm(self, config_id, number_value=None, slope_value=None):
        """
        告警
        """
        url = urlparse.urljoin('http://' + self.domain, ALARM_PATH)

        data = json.dumps(dict(
            config_id=config_id,
            number_value=number_value,
            slope_value=slope_value,
        ))

        sign = hashlib.md5('|'.join(self.secret, data)).hexdigest()

        rsp = requests.post(url, dict(
            data=data,
            sign=sign,
        ))

        if not rsp.ok:
            logger.error('fail. url: %s, data: %s, sign: %s', url, data, sign)
            return False

        return True
