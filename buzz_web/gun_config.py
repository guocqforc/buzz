proc_name = 'buzz_web'
# sync/gevent
worker_class = 'gevent'
bind = ['127.0.0.1:8000']
workers = 2
# for debug
#accesslog = '-'
#loglevel = 'debug'
#debug=True
