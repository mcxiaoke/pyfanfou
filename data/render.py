#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-12 23:02:46

from __future__ import print_function
import json
import shutil
from StringIO import StringIO

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

data = json.load(open('timeline.json', 'r'))
html.write(header)
for it in data:
    html.write(u'<div class="status">\n')
    html.write(u'<p class="status_text">{0}</p>\n'.format(it['text']))
    html.write(u'<p class="status_author">{0} {1}</p>\n'.format(it['user']['screen_name'], it['created_at']))
    html.write(u'</div>\n')
    html.write(u'<br />\n')

html.write(footer)
# http://stackoverflow.com/questions/6048085/python-write-unicode-text-to-a-text-file
with open('index.html','w') as out:
    out.write(html.getvalue().encode('utf8'))
