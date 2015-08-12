#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-12 09:03:09

from lib.backup import Backup
from lib.backup import parse_args


def start():
    Backup(**vars(parse_args())).start()

if __name__ == '__main__':
    start()
