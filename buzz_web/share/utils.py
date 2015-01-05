# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
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


def send_mail(receivers, subject, content):
    """
    发送邮件
    :param receivers:
    :return:
    """

    return _send_email(settings.MAIL_SERVER, settings.MAIL_USERNAME, settings.MAIL_PASSWORD,
                       settings.MAIL_SENDER, receivers, subject, content,
                       'plain', 'utf-8')


def _send_email(server, username, password, sender, receivers, subject, content, content_type, content_encoding):
    """
    content_tuple:
        (str, 'plain', utf-8)
        (str, 'html', utf-8)
    """
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    # 设定root信息
    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject
    msg_root['From'] = sender
    msg_root['To'] = ','.join(receivers)
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)

    msg_text = MIMEText(content, content_type, content_encoding)
    msg_alternative.attach(msg_text)

    # 发送邮件
    smtp = smtplib.SMTP()
    # 设定调试级别，依情况而定
    smtp.set_debuglevel(1)
    smtp.connect(server)
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg_root.as_string())
    smtp.quit()
    return True
