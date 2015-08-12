#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-07 23:13:33
'''
Run fanfou statuses backup command line.
'''
import sys
from backup.tools import Backup
from backup.tools import parse_args
if __name__ == '__main__':
    if len(sys.argv) < 2:
        options = {'target': 'androidsupport'}
        Backup(**options).start()
    else:
        Backup(**vars(parse_args())).start()
