#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50
'''
some scripts for fanfou.com
'''
import argparse
import utils
import time
from lib.api import ApiClient
from lib.api import ApiError
from db import DB
import os
import sys

DEFAULT_COUNT = 60

__version__ = '1.0.0'


def _fetch_newer_statuses(api, db, uid):
    # 增量更新
    head_status = db.get_latest_status()
    if head_status:
        while(True):
            head_status = db.get_latest_status()
            since_id = head_status['sid'] if head_status else None
            print 'fetch statuses for {0}, since_id: {1}'.format(uid, since_id)
            timeline = api.get_user_timeline(
                uid, count=DEFAULT_COUNT, since_id=since_id)
            if not timeline:
                break
            db.bulk_insert_status(timeline)
            time.sleep(2)
            if len(timeline) < DEFAULT_COUNT:
                break


def _fetch_older_statuses(api, db, uid):
    # then, check older status
    while(True):
        tail_status = db.get_oldest_status()
        max_id = tail_status['sid'] if tail_status else None
        print 'fetch statuses for {0}, max_id: {1}'.format(uid, max_id)
        timeline = api.get_user_timeline(
            uid, count=DEFAULT_COUNT, max_id=max_id)
        if not timeline:
            break
        db.bulk_insert_status(timeline)
        time.sleep(2)
        if len(timeline) < DEFAULT_COUNT:
            break


def backup(username=None, password=None, **options):
    auth_mode = username and password
    output = options['output'] or 'out'
    target = options.get('target')
    verbose = options.get('verbose') != None
    if not os.path.exists(output):
        os.mkdir(output)
    '''
    backup fanfou.com statuses data for target user.
    '''
    api = ApiClient(verbose)
    token = utils.load_account_info(username)
    if token:
        print 'load token for [{1}]: {0}'.format(
            token['oauth_token'], username)
        api.set_oauth_token(token)
    user = None
    if auth_mode:
        if api.is_verified():
            token = api.oauth_token
            user = api.user
        else:
            token = api.login(username, password)
            user = api.user
            print 'save new token for [{1}]: {0}'.format(
                token['oauth_token'], username)
            utils.save_account_info(username, token)
    if not target and not user:
        print 'Error: no target id found, exit'
        return
    target_id = target or user['id']
    print 'target user id is "%s" ' % target_id
    try:
        target_user = api.get_user(target_id)
    except ApiError,e:
        if e.args[0] == 404:
            print 'Error: target user: "{0}" not exists'.format(target_id)
        target_user = None
    if not target_user:
        print 'Error: unable to get user: "{0}", exit'.format(target_id)
        return
    print 'Starting backup statuses for user: "{0}"'.format(target_id)

    db_name = '{0}/{1}.db'.format(output, target_id)
    print 'db name is %s' % db_name
    db = DB(db_name)
    # first ,check new statuses
    _fetch_newer_statuses(api, db, target_id)
    # then, check older status
    _fetch_older_statuses(api, db, target_id)
    print 'all {0} statuses for {1} are stored in database'.format(
        db.get_status_count(), target_id)
    db.print_status()


def parse_args():
    '''
    parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        help='your fanfou.com account username')
    parser.add_argument('-p', '--password',
                        help='your fanfou.com account password')
    parser.add_argument('-t', '--target',
                        help='user id to backup, default is current user')
    parser.add_argument('-o', '--output',
                        help='output dir, default is ./output/')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show verbose process details')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    backup(**vars(parse_args()))
