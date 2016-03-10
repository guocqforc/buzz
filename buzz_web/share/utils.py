# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse


def jsonify(*args, **kwargs):
    """支持时间、日期的jsonify"""

    def _custom_dumps(o):
        import datetime
        import decimal

        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, datetime.time):
            return o.strftime('%H:%M:%S')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        else:
            raise TypeError(repr(o) + ' is not JSON serializable')

    encoded_data = json.dumps(
        dict(*args, **kwargs),
        ensure_ascii=False,
        default=_custom_dumps,
    )

    return HttpResponse(
        encoded_data,
        content_type='application/json'
    )


def sendmail(host, port, sender, receivers, subject, content,
             content_type='plain', encoding='utf-8',
             username=None, password=None, use_ssl=False, use_tls=False, debuglevel=0
             ):
    """
    发送邮件
    content_type: plain / html
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formatdate

    mail_msg = MIMEText(content, content_type, encoding)
    mail_msg['Subject'] = Header(subject, encoding)
    mail_msg['From'] = sender
    mail_msg['To'] = ', '.join(receivers)
    mail_msg['Date'] = formatdate()

    if use_ssl:
        mail_client = smtplib.SMTP_SSL(host, port)
    else:
        mail_client = smtplib.SMTP(host, port)

    mail_client.set_debuglevel(debuglevel)

    if use_tls:
        mail_client.starttls()

    if username and password:
        mail_client.login(username, password)

    # 发邮件
    mail_client.sendmail(sender, receivers, mail_msg.as_string())
    mail_client.quit()
