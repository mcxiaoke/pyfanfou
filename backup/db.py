#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 20:07:34

import utils
from lib.basedb import BaseDB

KV_TABLE = "kv"
LOG_TABLE = "log"
USER_TABLE = "user"
STATUS_TABLE = "status"

KV_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS kv '
    ' ( _id INTEGER PRIMARY KEY, '
    ' key TEXT, '
    ' value TEXT, '
    ' comment TEXT, '
    ' added_at TEXT'
    ' UNIQUE (key) ); '
)

LOG_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS log '
    ' ( _id INTEGER PRIMARY KEY, '
    ' tag TEXT, '
    ' action TEXT, '
    ' message TEXT, '
    ' comment TEXT, '
    ' added_at TEXT'
    ' UNIQUE (_id) ); '
)

USER_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS user '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id TEXT, '
    ' screen_name TEXT, '
    ' created_at TEXT, '
    ' added_at TEXT, '
    ' data TEXT, '
    ' UNIQUE (id) ); '
)

STATUS_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS status '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id INTEGER, '
    ' sid TEXT, '
    ' uid TEXT,'
    ' created_at TEXT, '
    ' added_at TEXT, '
    ' data TEXT, '
    ' UNIQUE (id) ); '
)


class DB(BaseDB):

    def __init__(self, db_name):
        super(DB, self).__init__(db_name)
        self._create_tables()

    def _create_tables(self):
        conn = self.conn
        conn.execute(USER_TABLE_CREATE_SQL)
        conn.execute(STATUS_TABLE_CREATE_SQL)
        conn.commit()

    def get_user_count(self):
        return self.get_count('user')

    def get_status_count(self):
        return self.get_count('status')

    def get_all_user_ids(self):
        rows = self.execute('select id from user').fetchall()
        ids = [row['id'] for row in rows]
        return ids

    def get_all_status_ids(self):
        rows = self.execute('select id from status').fetchall()
        ids = [row['id'] for row in rows]
        return ids

    def get_all_users(self):
        return self.fetch_all('user')

    def get_all_status(self):
        return self.fetch_all('status')

        # oldest user order by creation time
    def get_oldest_user(self):
        c = self.execute("select id,screen_name,created_at from user "
                         "order by created_at ASC limit 1;")
        return c.fetchone()

        # oldest status order by creation time
    def get_oldest_status(self):
        c = self.execute("select id,sid,created_at from status "
                         "order by created_at ASC limit 1;")
        return c.fetchone()

        # latest user order by creation time
    def get_latest_user(self):
        c = self.execute("select id,screen_name,created_at from user "
                         "order by created_at DESC limit 1;")
        return c.fetchone()

        # latest status order by creation time
    def get_latest_status(self):
        c = self.execute("select id,sid,created_at from status " +
                         "order by created_at DESC limit 1;")
        return c.fetchone()

    def insert_user(self, user):
        values = utils.convert_user(user)
        c = self.conn.cursor()
        c.execute(("INSERT OR REPLACE INTO user "
                   " (id,screen_name,created_at,added_at,data) "
                   " VALUES (?,?,?,?,?) "), *values)
        print "insert_user: %d rows inserted to database" % c.rowcount
        self.conn.commit()
        return c

    def bulk_insert_user(self, user_list):
        values = [utils.convert_user(user) for user in user_list]
        c = self.conn.cursor()
        c.executemany(("INSERT OR REPLACE INTO user "
                       " (id,screen_name,created_at,added_at,data) "
                       " VALUES (?,?,?,?,?) "), values)
        print "bulk_insert_user: %d rows inserted to database" % c.rowcount
        self.conn.commit()
        return c

    def insert_status(self, status):
        values = utils.convert_status(status)
        c = self.conn.cursor()
        c.execute(("INSERT OR REPLACE INTO status "
                   " (id,sid,uid,created_at,added_at,data) "
                   " VALUES (?,?,?,?,?,?) "), *values)
        self.conn.commit()
        print "insert_status: %d rows inserted to database" % c.rowcount
        return c

    def bulk_insert_status(self, status_list):
        values = [utils.convert_status(status) for status in status_list]
        c = self.conn.cursor()
        c.executemany(("INSERT OR REPLACE INTO status "
                       " (id,sid,uid,created_at,added_at,data) "
                       " VALUES (?,?,?,?,?,?) "), values)
        self.conn.commit()
        print "bulk_insert_status: %d rows inserted to database" % c.rowcount
        return c

    def print_status(self):
        # print 'users count:', self.get_user_count()
        # print 'oldest user:', self.get_oldest_user()
        # print 'latest user:', self.get_latest_user()
        print "====== database statictics start ======"
        print 'status count:', self.get_status_count()
        print 'oldest status:', self.get_oldest_status()
        print 'latest status:', self.get_latest_status()
        print "====== database statictics end ======"


if __name__ == '__main__':
    import sys
    db = DB(sys.argv[1])
    db.print_status()
    db.close()
