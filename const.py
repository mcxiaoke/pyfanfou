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
