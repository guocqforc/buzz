# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
from django.conf import settings

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


def send_mail(receivers, subject, content, content_type='plain'):
    """
    发送邮件
    :param receivers:
    :return:
    """
    authInfo = {}
    authInfo['server'] = settings.MAIL_SERVER
    authInfo['user'] = settings.MAIL_USERNAME
    authInfo['password'] = settings.MAIL_PASSWORD
    fromAdd = settings.MAIL_SENDER
    toAdd = receivers
    subject = subject
    content_tuple = (content, content_type, 'utf-8')
    _send_email(authInfo, fromAdd, toAdd, subject, content_tuple)


def _send_email(authInfo, fromAdd, toAdd, subject, content_tuple):
    """
    content_tuple:
        (str, 'plain', utf-8)
        (str, 'html', utf-8)
    """

    strFrom = fromAdd
    strTo = ', '.join(toAdd)

    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd) :
            print 'incomplete login info, exit now'
            return

    # 设定root信息
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(*content_tuple)
    msgAlternative.attach(msgText)

    #发送邮件
    smtp = smtplib.SMTP()
    #设定调试级别，依情况而定
    smtp.set_debuglevel(1)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return
