# -*- coding: utf-8 -*-

import datetime
import urlparse
import logging
import os.path
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
            return False

        now = datetime.datetime.now()

        for conf in self.alarm_config:
            stat_path = os.path.join(self.path, conf['stat_name'].replace('.', '/'))
            logger.debug('stat_path: %s', stat_path)

            try:
                (timeInfo, values) = whisper.fetch(stat_path, self.last_run_time, now)
            except:
                logger.error('exc occur. stat_path: %s, conf: %s', stat_path, conf, exc_info=True)

    def _load_config(self):
        """
        读取配置
        :return:
        """

        url = urlparse.urljoin('http://' + self.domain, LOAD_CONFIG_PATH)

        rsp = requests.get(url)
        if not rsp.ok:
            return False

        self.alarm_config = rsp.json()

        return True
