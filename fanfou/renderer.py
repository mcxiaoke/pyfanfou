#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-12 23:02:46

from __future__ import print_function
import json
import time
import shutil
import os
import sys
from cStringIO import StringIO
from string import Template
import template
import utils


def _render_status_html(it, out, outDir):
    id = it['id']
    name = it['user']['screen_name']
    uid = it['user']['id']
    raw_time = it['created_at']
    time = utils.get_only_fanfou_date(raw_time).decode('utf8')
    text = it['text']
    if it.get('photo'):
        imgfile = os.path.join('{0}-photos'.format(uid), '{0}.jpg'.format(id))
        imgpath = os.path.join(outDir, imgfile)
        photo = imgfile if os.path.exists(imgpath) else it['photo']['url']
    else:
        photo = ''
    tpl = Template(template.STATUS_TEMPLATE)
    status = tpl.substitute(id=id, name=name, uid=uid,
                            raw_time=raw_time, time=time,
                            text=text, photo_url=photo,
                            photo_link=u'照片' if photo else '')
    out.write(status.encode('utf8'))


def _render_html(data, outDir):
    first = data[0]
    user = first['user']
    title = u'{0}的消息'.format(user['screen_name'])
    out = StringIO()
    out.write(Template(template.HEAD).substitute(title=title).encode('utf8'))
    out.write(Template(template.BODY_HEADER).substitute(
        title=title).encode('utf8'))
    out.write(u'<div class="timeline">')
    for it in data:
        #print('render status ',it['id'])
        _render_status_html(it, out, outDir)

    out.write(u'</div>')
    out.write(template.BODY_FOOTER)
    return out.getvalue()


def _render_status_makrdown(it, out):
    id = it['id']
    name = it['user']['screen_name']
    uid = it['user']['id']
    raw_time = it['created_at']
    time = utils.normalize_fanfou_date(raw_time).decode('utf8')
    text = it['text']
    photo = u' [图片] ' if it.get('photo') else u''
    tpl = Template(template.MARKDOWN_STATUS)
    status = tpl.substitute(id=id, name=name, uid=uid,
                            time=time, text=text, photo=photo)
    out.write(status.encode('utf8'))


def _render_markdown(data):
    first = data[0]
    user = first['user']
    title = u'{0}的消息'.format(user['screen_name'])
    out = StringIO()
    out.write(Template(template.MARKDOWN_HEADER).substitute(
        title=title).encode('utf8'))
    for it in data:
        _render_status_makrdown(it, out)

    out.write(template.MARKDOWN_FOOTER)
    return out.getvalue()


def _render_status_text(it, out):
    id = it['id']
    name = it['user']['screen_name']
    uid = it['user']['id']
    raw_time = it['created_at']
    time = utils.get_only_fanfou_date(raw_time).decode('utf8')
    text = it['text']
    tpl = Template(template.TEXT_STATUS)
    status = tpl.substitute(id=id, name=name, uid=uid, time=time, text=text)
    out.write(status.encode('utf8'))


def _render_text(data):
    first = data[0]
    user = first['user']
    title = u'{0}的消息'.format(user['screen_name'])
    out = StringIO()
    out.write(Template(template.TEXT_HEADER).substitute(
        title=title).encode('utf8'))
    for it in data:
        _render_status_text(it, out)

    out.write(template.TEXT_FOOTER)
    return out.getvalue()


def render(data, fileOut):
    output = os.path.dirname(fileOut)
    # inData = json.load(open(fileIn, 'r'))
    html = _render_html(data, output)
    markdown = _render_markdown(data)
    text = _render_text(data)
    # http://stackoverflow.com/questions/6048085/python-write-unicode-text-to-a-text-file
    # save  html
    tempfile = os.path.join(unicode(time.time()))
    with open(tempfile, 'w') as out:
        out.write(html)
    shutil.move(tempfile, fileOut+'.html')
    # save markdown
    tempfile = os.path.join(unicode(time.time()))
    with open(tempfile, 'w') as out:
        out.write(markdown)
    shutil.move(tempfile, fileOut+'.md')
    # save text
    tempfile = os.path.join(unicode(time.time()))
    with open(tempfile, 'w') as out:
        out.write(text)
    shutil.move(tempfile, fileOut+'.txt')


if __name__ == '__main__':
    # json.load(open('data/timeline.json','r'))
    render(json.load(open('../data/timeline.json', 'r')),
           '../data/timeline')
