#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-12 23:02:46

from __future__ import print_function
import json
import shutil
from StringIO import StringIO
from fanfou import utils

html = StringIO()

header = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="timeline.css" />
    </head>
    <body>
'''

footer = '''
    </body>
</html>
'''

data = json.load(open('data/timeline.json', 'r'))
html.write(header)
for it in data:
    pretty_date = utils.pretty_fanfou_date(it['created_at']).decode('utf8')
    html.write(u'<div class="status" id="status_{0}">\n'.format(it['id']))
    html.write(u'''<div class="status_author">\n
        <p class="status_author_name">{0}</p>\n
        <p class="status_author_id">(@{1})</p>\n
        <p class="status_author_time">{2}</p>\n
        </div>\n'''.format(it['user']['screen_name'], it['user']['id'], pretty_date))
    html.write(
        u'<p class="status_text">{0}</p>\n'.format(it['text']))
    html.write(u'</div>\n')
    html.write(u'<br />\n')

html.write(footer)
# http://stackoverflow.com/questions/6048085/python-write-unicode-text-to-a-text-file
with open('data/index.html', 'w') as out:
    out.write(html.getvalue().encode('utf8'))
