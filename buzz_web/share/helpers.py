# -*- coding: utf-8 -*-

from flylog import Client
from django.conf import settings

flylog_client = Client(settings.FLYLOG_HOST, settings.FLYLOG_PORT)
