#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 22:18:00
from __future__ import print_function
from datetime import datetime
import time
import pickle as store
import json
import requests
import cStringIO

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
    followers_count = user['followers_count']
    followings_count = user['friends_count']
    statuses_count = user['statuses_count']
    data = json.dumps(user)
    return (id, screen_name, followers_count, followings_count,
            statuses_count, created_at, added_at, data)


def convert_status(status):
    id = status["rawid"]
    sid = status['id']
    user = status['user']
    uid = user['id']
    text = status['text']
    created_at = normalize_fanfou_date(status["created_at"])
    added_at = get_now_datetime_str()
    data = json.dumps(status)
    return (id, sid, uid, text, created_at, added_at, data)


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


def pretty_fanfou_date(date_str):
    dt = parse_fanfou_date(date_str)
    return pretty_date(dt)

def pretty_date(time=None):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return str(second_diff) + " 秒前"
        if second_diff < 120:
            return "1一分钟前"
        if second_diff < 3600:
            return str(second_diff / 60) + " 分钟前"
        if second_diff < 7200:
            return "1小时前"
        if second_diff < 86400:
            return str(second_diff / 3600) + " 小时前"
    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return str(day_diff) + " 天前"
    if day_diff < 31:
        return str(day_diff / 7) + " 周前"
    if day_diff < 365:
        return str(day_diff / 30) + " 个月前"
    return str(day_diff / 365) + " 年前"


def download_and_save(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)


if __name__ == '__main__':
    date_str = "Sat May 12 14:24:26 +0000 2007"
    fd1 = parse_fanfou_date(date_str)
    fd2 = normalize_fanfou_date(date_str)
    nd1 = normalize_timestamp(time.time())
    nd2 = normalize_datetime(datetime.now())
    dt1 = parse_normalize_date(fd2)
    dt2 = parse_normalize_date(nd2)
    print(fd1)
    print(fd2)
    print(dt1)
    print(nd1)
    print(nd2)
    print(dt2)
    print(normalize_datetime(datetime.now()))
    print(pretty_date(fd1))

