#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 21:02:43
APP_NAME = '饭否数据备份工具'
APP_VERSION = '1.0.0'

AUTH_DESCRIPTION = u'''
说明：备份公开用户的数据不需要帐号和密码，此时请指定目标用户的ID。备份私密用户的数据需要有权限，如果是你自己的数据，需要登录，如果是别人的数据，需要是你关注的人，否则无法读取消息数据。
'''

NO_INPUT_TITLE = '错误提示'
NO_INPUT_MESSAGE = '请输入帐号密码或目标用户ID，至少输入一项！'

LOGIN_FIELDS = ['饭否帐号：', '饭否密码：', '目标用户：']
LOGIN_COMMENTS = ['*备份私密帐号数据必填', '*备份私密帐号数据必填', '*要备份的用户ID（可选）']

USER_GUIDE = '''
================================================

饭否数据备份工具 by mcxiaoke

使用说明：
1. 备份公开用户的数据不需要帐号和密码，此时请指定目标用户的ID。
2. 备份私密用户的数据需要有权限，如果是你自己的数据，需要登录。
3. 如果要备份别人的数据，需要是你关注的人，否则无法读取数据。

简单地说，你在网页上能看到的消息和照片，就是可以备份的。

（备份中途可随时停止，本工具会自动增量备份，不会重复下载）

备份输出的数据格式为SQLite数据库文件，HTML格式+TXT格式+Markdown格式

======== 饭否数据备份工具 v1.0.0 ========

命令行使用：
fanfoubackup.py [-h] [-u USERNAME] [-p PASSWORD] [-t TARGET] [-s] [-i]
                 [-o OUTPUT]

  -h, --help   显示帮助信息
  -u USERNAME, --username USERNAME 你的饭否帐号
  -p PASSWORD, --password PASSWORD 你的饭否密码
  -t TARGET, --target TARGET 要备份的用户ID，默认是登录帐号
  -s , --include-user 是否备份好友资料列表，默认否
  -i , --include-photo 是否备份全部相册照片，默认是
  -o OUTPUT, --output OUTPUT 备份数据存放目录，默认是当前目录下的output目录

项目地址：
https://github.com/mcxiaoke/pyfanfou

================================================
'''
