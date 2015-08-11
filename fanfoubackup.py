#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-07 23:13:33
'''
Run fanfou statuses backup command line.
'''
from backup.tools import backup
from backup.tools import parse_args
if __name__ == '__main__':
    backup(**vars(parse_args()))
