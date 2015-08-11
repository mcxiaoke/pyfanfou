#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 15:45:36
from __future__ import print_function


def test(*args, **kwargs):
    print(args)
    print(kwargs)
    print(kwargs['hello'])
    print(kwargs.get('no'))
    print(kwargs.get('none', 'default'))


d = {}
d['hello'] = 2015
d['str'] = 'message'
d['value'] = True
d['none'] = None

test([1, 2, 3, 4, 5], **d)
