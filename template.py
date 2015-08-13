#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-13 11:20:23

HEAD = u'''<!DOCTYPE html>
<html lang="zh_CN">
    <head>
        <title>饭否消息备份</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style type="text/css">
            html,body,p {
                font-size: 100%;
                padding: 0;
                margin: 0;
            }
            body{
                background-color:#2183B4;
            }
            .header{
               margin:0px auto;
               padding:24px; 
               width:60%;
            }
            .header p{
                color:#ffffff;
                font-size:150%;
                text-align:center;
                margin:16px;
            }
            .footer{
                margin:0px auto;
                padding 8px;
                width:60%;
            }
            .footer p{
                color:#ffffff;
                font-size:50%;
                text-align:center;
                margin:16px;
            }
            .footer a{
                text-decoration: none;
                color:#ffffff;
            }
            .timeline{
                 margin:0px auto;
                 width:640px;
                 background-color: #ffffff;
            }
            .status{
                 margin:0px auto;
                 padding: 16px;
                 width:540px;
                 height:100%;
                 border-bottom:1px dashed #e0e0e0;
            }
            .st_text{
                color:#4B585D;
            }
            .st_meta{
                font-size: 80%;
                margin-bottom: 8px;
            }
            .st_name {
                color: #3F9ECD;
                font-weight: bold;
            }
            .st_uid {
                color: #999999;
            }
            .st_time{
                font-size: 70%;
                margin-left: 8px;
                color:#999999;
            }
        </style>
    </head>
'''

BODY_HEADER = u'''
    <body>
    <div class="header">{0}</div>
'''
BODY_FOOTER = u'''
    <div class="footer">{0}</div>
    </body>
</html>
'''
