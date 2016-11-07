buzz
====

alarm system for statsd and graphite.

### 一. 概述

项目主要分为两部分: buzz_web 和 buzz_agent ，简要描述如下:


* buzz_web

    配置告警，支持值类型和波动率类型，可指定运维组或者单个运维人员接收告警，告警方式为邮件。

    每条记录的name即statsd的路径，如: stats.gauges.app.connections.login

    每条配置记录同时支持支持值类型、波动率、差值，不同类型之间是"与"的关系，也可以只配置其中一个。

    每条配置记录之间为"或"的关系。

    波动率和差值区分正值和负值，比如 > 0.1 和 < -0.1，需要分开来配置。

    对于gauge类型:
        值: 上报的数值
        波动率: 上报数值相比上一次的波动比率
        差值: 上报数值相比上一次的变化值

    对于incr类型:
        值: 上报的数值，即每次的变化量
        波动率： 上报的数值的波动率
        差值: 上报数值的差值

* buzz_agent

    分析statsd数据，并从buzz_web拉取告警配置信息。
    
    经过匹配过滤之后，将需要告警的数据发送给buzz_web。

    需要启动在statsd数据所在的位置。


### 二. 示例

buzz_web某条告警配置:

    name: stats.gauges.app.connections.login
    值类型比较符: 大于等于
    值类型数值: 100
    波动率比较符: 小于等于
    波动率数值: -0.1
    差值比较符: 大于等于
    差值数值: 100
    告警组: 运维组


### 三. 部署依赖

buzz_web:

    flylog

buzz_agent:

    requests
