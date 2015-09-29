buzz
====

alarm system for statsd and graphite.

### 一. 概述

项目主要分为两部分: buzz_web 和 buzz_agent ，简要描述如下:  


* buzz_web

    配置告警，支持值类型和波动率类型，可指定运维组或者单个运维人员接收告警，告警方式为邮件。

    每条记录的name即statsd的路径，如: stats.gauges.texas.CN.connections.login

    每条配置记录同时支持支持值类型和波动率，值类型与波动率是"与"的关系，也可以只配置其中一个。

    每条配置记录之间为"或"的关系。

    波动率支持正值和负值，比如 > 0.1 和 < -0.1，需要分开来配置。

* buzz_agent

    分析statsd数据，并从buzz_web拉取告警配置信息。
    
    经过匹配过滤之后，将需要告警的数据发送给buzz_web。

    需要启动在statsd数据所在的位置。


### 二. 示例

buzz_web某条告警配置:

    name: stats.gauges.texas.CN.connections.login
    值类型比较符: 大于等于
    值类型数值: 100
    波动率比较符: 小于等于
    波动率数值: -0.1
    告警组: 运维组
