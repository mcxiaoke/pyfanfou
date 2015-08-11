#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50
from __future__ import print_function
'''
饭否数据处理脚本
'''
import argparse
import utils
import time
from lib.api import ApiClient
from lib.api import ApiError
from db import DB
import os
import logging

DEFAULT_COUNT = 60

__version__ = '1.0.0'

logger = logging.getLogger(__name__)


def _fetch_newer_statuses(api, db, uid):
    '''增量更新，获取比某一条新的数据（新发布的）'''
    count = 0
    head_status = db.get_latest_status()
    if head_status:
        while(True):
            head_status = db.get_latest_status()
            since_id = head_status['sid'] if head_status else None
            timeline = api.get_user_timeline(
                uid, count=DEFAULT_COUNT, since_id=since_id)
            if not timeline:
                break
            print("抓取到用户[{0}]的{1}条消息，准备保存...".format(uid, len(timeline)))
            db.bulk_insert_status(timeline)
            count += len(timeline)
            time.sleep(2)
            if len(timeline) < DEFAULT_COUNT:
                break
    return count


def _fetch_older_statuses(api, db, uid):
    '''增量更新，获取比某一条旧的数据'''
    count = 0
    while(True):
        tail_status = db.get_oldest_status()
        max_id = tail_status['sid'] if tail_status else None
        timeline = api.get_user_timeline(
            uid, count=DEFAULT_COUNT, max_id=max_id)
        if not timeline:
            break
        print("抓取到用户[{0}]的{1}条消息，准备保存...".format(uid, len(timeline)))
        db.bulk_insert_status(timeline)
        count += len(timeline)
        time.sleep(2)
        if len(timeline) < DEFAULT_COUNT:
            break
    return count


def backup(username=None, password=None, **options):
    '''
    备份饭否指定用户的饭否消息数据

    username - 用户帐号（可选）
    password - 用户密码（可选）
    output - 数据保存目录
    target - 目标用户ID
    '''
    auth_mode = username and password
    output = options['output'] or 'output'
    target = options.get('target')
    verbose = options.get('verbose') != None
    if not os.path.exists(output):
        os.mkdir(output)
    api = ApiClient(verbose)
    token = utils.load_account_info(username)
    if token:
        print('载入用户[{1}]的本地登录信息 [{0}]'.format(
            token['oauth_token'], username))
        api.set_oauth_token(token)
    user = None
    if auth_mode:
        if api.is_verified():
            token = api.oauth_token
            user = api.user
        else:
            token = api.login(username, password)
            user = api.user
            print('保存用户[{1}]的登录信息 [{0}]'.format(
                token['oauth_token'], username))
            utils.save_account_info(username, token)
    if not target and not user:
        print('没有指定要备份的用户')
        return
    target_id = target or user['id']
    try:
        target_user = api.get_user(target_id)
    except ApiError, e:
        if e.args[0] == 404:
            print('你指定的用户[{0}]不存在'.format(target_id))
        target_user = None
    if not target_user:
        print(
            '无法获取用户[{0}]的信息'.format(target_id))
        return
    print('开始备份用户[{0}]的消息数据...'.format(target_id))
    db_file = os.path.abspath('{0}/{1}.db'.format(output, target_id))
    print('用户数据备份位置：{0}'.format(db_file))
    db = DB(db_file)
    total = 0
    # first ,check new statuses
    total += _fetch_newer_statuses(api, db, target_id)
    # then, check older status
    total += _fetch_older_statuses(api, db, target_id)

    if total:
        print('用户[{1}]的全部{0}条消息已保存'.format(
            db.get_status_count(), target_id))
    else:
        print('用户[{0}]的全部消息已保存，没有新增消息'.format(target_id))


def parse_args():
    '''
    解析命令行参数
    '''
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='饭否数据备份工具 v{0}'.format(__version__),
        epilog='''项目主页 https://github.com/mcxiaoke/pyfanfou
        ''')
    parser.add_argument('-u', '--username',
                        help='你的饭否帐号')
    parser.add_argument('-p', '--password',
                        help='你的饭否密码')
    parser.add_argument('-t', '--target',
                        help='要备份的用户ID，默认是登录帐号')
    parser.add_argument('-o', '--output',
                        help='备份数据存放目录，默认是当前目录下的output目录')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    backup(**vars(parse_args()))
