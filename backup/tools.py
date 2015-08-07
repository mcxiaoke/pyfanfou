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

DEFAULT_COUNT = 60

__version__ = '1.0.0'


def _fetch_newer_statuses(api, uid):
    # first ,check new statuses
    db = DB('{0}.db'.format(uid))
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


def _fetch_older_statuses(api, uid):
    # then, check older status
    db = DB('{0}.db'.format(uid))
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


def backup(username=None, password=None, userid=None, verbose=False):
    '''
    backup fanfou.com statuses data for target user.
    '''
    if not username or not password:
        print 'invalid account ({0}, {1})'.format(username, password)
        return
    api = ApiClient(verbose)
    token = utils.load_account_info(username)
    if token:
        print 'load token for [{1}]: {0}'.format(
            token['oauth_token'], username)
        api.set_oauth_token(token)
    if api.is_verified():
        token = api.oauth_token
        user = api.user
    else:
        token = api.login(username, password)
        if token:
            user = api.user
            print 'save new token for [{1}]: {0}'.format(
                token['oauth_token'], username)
            utils.save_account_info(username, token)
        else:
            return
    target_id = userid if userid else user['id']
    try:
        target_user = api.get_user(target_id)
    except ApiError:
        target_user = None
    if not target_user:
        print 'Error: unable to get user info: "{0}", exit'.format(target_id)
        return
    print 'starting backup statuses for user: "{0}"'.format(target_id)
    # first ,check new statuses
    _fetch_newer_statuses(api, target_id)
    # then, check older status
    _fetch_older_statuses(api, target_id)
    db = DB('{0}.db'.format(target_id))
    print 'all {0} statuses for {1} are stored in database'.format(
        db.get_status_count(), target_id)
    db.print_status()


def parse_args():
    '''
    parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'username', help='your fanfou.com account username')
    parser.add_argument(
        'password', help='your fanfou.com account password')
    parser.add_argument('-u', '--userid',
                        help='user id to backup, default is current user')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show verbose process details')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    backup(**vars(parse_args()))
