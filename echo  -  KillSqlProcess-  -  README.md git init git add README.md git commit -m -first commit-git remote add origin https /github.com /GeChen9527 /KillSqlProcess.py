#!/usr/bin/python
# -*- coding:UTF-8 -*-
import pymysql
import logging

#数据库连接
connection = pymysql.connect(host='host',port=port,user='user',
                             password='pwd',db='db',
                             )
#创建游标
cursor = connection.cursor()

#定义日志格式
logging.basicConfig(
    level=logging.DEBUG,#日志输出级别
    format='%(asctime)s %(filename)s : %(levelname)s --%(message)s',#日志格式
    datefmt='%Y-%m-%d %H:%M:%S',#日志时间
    filename='/var/log/killmysql/killmysql.log',#日志路径
    filemode='a'#写入方式
)
#查询执行进程并传值给元组List
cursor.execute("show processlist;")
for List in cursor.fetchall():
#判断超时语句是否是sleep并输出日志
    if List[5] > 2 and List[4] == 'Query': ##修改query时一定要慎重，避免误kill
        pid = List[0]
        sql = List[7]
        cursor.execute("kill %s;", pid)
        logging.info('Kill Pid is %s Sql:%s', pid, sql)

#关闭数据库连接
cursor.close()
connection.close()
