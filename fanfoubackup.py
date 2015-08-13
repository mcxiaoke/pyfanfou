#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-07 23:13:33
'''
Run fanfou statuses backup.
'''
import sys
import backupcmd
import backupui

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-gui':
        backupui.start()
    else:
        backupcmd.start()
