#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-12 23:02:46

from __future__ import print_function
import json
from StringIO import StringIO
import template
from string import Template
from fanfou import utils


def _render_status(it, out):
    id = it['id']
    name = it['user']['screen_name']
    uid = it['user']['id']
    raw_time = it['created_at']
    time = utils.pretty_fanfou_date(raw_time).decode('utf8')
    text = it['text']
    tpl = Template(template.STATUS_TEMPLATE)
    status = tpl.substitute(id=id, name=name, uid=uid,
                            raw_time=raw_time, time=time, text=text)
    # print(s.encode('utf8'))
    out.write(status)


def _render(data):
    first = data[0]
    user = first['user']
    title = u'{0}的饭否消息'.format(user['screen_name'])
    out = StringIO()
    out.write(Template(template.HEAD).substitute(title=title))
    out.write(Template(template.BODY_HEADER).substitute(title=title))
    out.write(u'<div class="timeline">')
    for it in data:
        _render_status(it, out)

    out.write(u'</div>')
    out.write(template.BODY_FOOTER)
    return out.getvalue().encode('utf8')


def render(fileIn, fileOut):
    inData = json.load(open(fileIn, 'r'))
    outData = _render(inData)
    # http://stackoverflow.com/questions/6048085/python-write-unicode-text-to-a-text-file
    with open(fileOut, 'w') as out:
        out.write(outData)


if __name__ == '__main__':
    # json.load(open('data/timeline.json','r'))
    render('data/timeline.json', 'data/timeline.html')
