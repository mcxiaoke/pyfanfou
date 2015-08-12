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
from api import ApiClient
from api import ApiError
from db import DB
import os
import logging

DEFAULT_COUNT = 60
DEFAULT_USER_COUNT = 100

__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class Backup(object):

    def __init__(self, **options):
        '''
        备份指定用户的饭否消息数据
        '''
        self._parse_options(**options)
        self.api = ApiClient(False)
        self.token = utils.load_account_info(self.username)
        self.user = None
        self.target_id = None
        self.db = None
        self.cancelled = False
        self.total = 0
        self.user_total = 0

    def _parse_options(self, **options):
        '''
        username - 用户帐号（可选）
        password - 用户密码（可选）
        output - 数据保存目录
        target - 目标用户ID
        '''
        self.username = options.get('username')
        self.password = options.get('password')
        self.auth_mode = self.username and self.password
        self.target = options.get('target')
        self.output = options.get('output') or 'output'

    def _precheck(self):
        if self.token:
            print('载入用户 [{1}] 的本地登录信息 [{0}]'.format(
                self.token['oauth_token'], self.username))
            self.api.set_oauth_token(self.token)
        if self.auth_mode:
            if self.api.is_verified():
                self.token = self.api.oauth_token
                self.user = self.api.user
            else:
                self.token = self.api.login(self.username, self.password)
                self.user = self.api.user
                print('保存用户 [{1}] 的登录信息 [{0}]'.format(
                    self.token['oauth_token'], self.username))
                utils.save_account_info(self.username, self.token)
        if not self.target and not self.user:
            print('没有指定备份的目标用户')
            return
        self.target_id = self.target or self.user['id']

    def stop(self):
        print('收到终止备份的命令，即将停止...')
        self.cancelled = True

    def start(self):
        self._precheck()
        if not self.target_id:
            return
        try:
            target_user = self.api.get_user(self.target_id)
        except ApiError, e:
            if e.args[0] == 404:
                print('你指定的用户 [{0}] 不存在'.format(self.target_id))
            target_user = None
        if not target_user:
            print(
                '无法获取用户 [{0}] 的信息'.format(self.target_id))
            return
        print('用户 [{0}] 共有 [{1}] 条消息'.format(
            target_user['id'], target_user['statuses_count']))
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        print('开始备份用户 [{0}] 的消息...'.format(self.target_id))
        db_file = os.path.abspath(
            '{0}/{1}.db'.format(self.output, self.target_id))
        print('数据路径：{0}'.format(db_file))
        self.db = DB(db_file)
        db_count = self.db.get_status_count()
        if db_count:
            print('发现数据库已备份消息 {0} 条'.format(db_count))
        # first ,check new statuses
        self._fetch_newer_statuses()
        # then, check older status
        self._fetch_older_statuses()
        # check user followings
        self._fetch_followings()
        self._report()
        if self.cancelled:
            print('本次备份已终止')
        else:
            print('本次备份已完成')
        self.db.close()

    def _report(self):
        if self.total:
            print('本次共备份 [{1}] 的 {0} 条消息'.format(
                self.db.get_status_count(), self.target_id))
        else:
            print('用户 [{0}] 的消息已备份，没有新增消息'.format(self.target_id))

    def _fetch_followings(self):
        '''全量更新，获取全部好友数据'''
        page = 0
        while(not self.cancelled):
            users = self.api.get_friends(self.target_id, page=page)
            if not users:
                break
            count = len(users)
            print("正在保存用户资料 {0}~{1}...".format(
                self.user_total, self.user_total+count))
            self.db.bulk_insert_user(users)
            self.user_total += count
            page += 1
            time.sleep(1)
            if len(users) < DEFAULT_USER_COUNT:
                break

    def _fetch_newer_statuses(self):
        '''增量更新，获取比某一条新的数据（新发布的）'''
        head_status = self.db.get_latest_status()
        if head_status:
            while(not self.cancelled):
                head_status = self.db.get_latest_status()
                since_id = head_status['sid'] if head_status else None
                timeline = self.api.get_user_timeline(
                    self.target_id, count=DEFAULT_COUNT, since_id=since_id)
                if not timeline:
                    break
                count = len(timeline)
                print("正在保存消息 {0}~{1}...".format(self.total, self.total+count))
                self.db.bulk_insert_status(timeline)
                self.total += count
                time.sleep(1)
                if len(timeline) < DEFAULT_COUNT:
                    break

    def _fetch_older_statuses(self):
        '''增量更新，获取比某一条旧的数据'''
        while not self.cancelled:
            tail_status = self.db.get_oldest_status()
            max_id = tail_status['sid'] if tail_status else None
            timeline = self.api.get_user_timeline(
                self.target_id, count=DEFAULT_COUNT, max_id=max_id)
            if not timeline:
                break
            count = len(timeline)
            print("正在保存消息 {0}~{1}...".format(self.total, self.total+count))
            self.db.bulk_insert_status(timeline)
            self.total += count
            time.sleep(1)
            if len(timeline) < DEFAULT_COUNT:
                break


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
    Backup(**vars(parse_args())).start()
