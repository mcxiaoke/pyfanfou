#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 22:18:00

from datetime import datetime
import time
import cPickle as store
import json

ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FANFOU_DATE_FORMAT = "%a %b %d %H:%M:%S +0000 %Y"


def save_account_info(username, token):
    if username and token:
        file_name = 'account_%s.dat' % username
        f = open(file_name.replace("@", "_"), 'wb')
        with f:
            store.dump(token, f)


def load_account_info(username):
    file_name = 'account_%s.dat' % username
    try:
        f = open(file_name.replace("@", "_"), 'rb')
        with f:
            return store.load(f)
    except IOError:
        pass


def convert_user(user):
    id = user["id"]
    screen_name = user["screen_name"]
    created_at = normalize_fanfou_date(user["created_at"])
    added_at = get_now_datetime_str()
    data = json.dumps(user)
    return (id, screen_name, created_at, added_at, data)


def convert_status(status):
    id = status["rawid"]
    sid = status['id']
    user = status['user']
    uid = user['id']
    created_at = normalize_fanfou_date(status["created_at"])
    added_at = get_now_datetime_str()
    data = json.dumps(user)
    return (id, sid, uid, created_at, added_at, data)


def parse_fanfou_date(date_str):
    return datetime.strptime(date_str, FANFOU_DATE_FORMAT)


def normalize_fanfou_date(date_str):
    return normalize_datetime(parse_fanfou_date(date_str))


def parse_normalize_date(date_str):
    return datetime.strptime(date_str, ISO_DATE_FORMAT)


def normalize_datetime(dt):
    return dt.strftime(ISO_DATE_FORMAT)


def normalize_timestamp(ts):
    return normalize_datetime(datetime.fromtimestamp(ts))


def get_now_datetime_str():
    return normalize_datetime(datetime.now())

if __name__ == '__main__':
    date_str = "Sat May 12 14:24:26 +0000 2007"
    fd1 = parse_fanfou_date(date_str)
    fd2 = normalize_fanfou_date(date_str)
    nd1 = normalize_timestamp(time.time())
    nd2 = normalize_datetime(datetime.now())
    dt1 = parse_normalize_date(fd2)
    dt2 = parse_normalize_date(nd2)
    print fd1
    print fd2
    print dt1
    print nd1
    print nd2
    print dt2
    print normalize_datetime(datetime.now())
