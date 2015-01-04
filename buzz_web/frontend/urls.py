# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^config$', 'frontend.views.load_config'),
                       url(r'^alarm$', 'frontend.views.send_alarm'),
)
