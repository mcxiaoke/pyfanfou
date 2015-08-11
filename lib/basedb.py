#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-07 07:36:01
import sqlite3


class BaseDB(object):

    def __init__(self, db_name):
        self.name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def fetch_all(self, table_name):
        return self.conn.execute(
            'select * from %s;' % table_name).fetchall()

    def get_count(self, table_name):
        return self.conn.execute(
            'select count() from %s;' % table_name).fetchone()[0]

    def execute(self, operation):
        c = self.conn.cursor()
        c.execute(operation)
        self.conn.commit()
        return c
