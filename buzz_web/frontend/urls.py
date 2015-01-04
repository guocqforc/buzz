# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'mysite.views.home', name='home'),
)
