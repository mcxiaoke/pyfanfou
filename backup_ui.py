#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 20:01:02
from __future__ import print_function
import textwrap
import sys
import os
import threading
import subprocess
import Queue as queue
from Tkinter import *
from ttk import Separator
from tkFileDialog import *
from tkSimpleDialog import *
from tkMessageBox import showerror, showinfo
from ScrolledText import ScrolledText
import const
from backup import tools
from imp import reload

__version__ = const.APP_VERSION


class GuiOutput:
    font = ('courier', 10, 'normal')

    def __init__(self, output):
        self.stdout = sys.stdout
        self.output = output

    def write(self, text):
        # self.stdout.write(text)
        self.output.write(text)

    def writelines(self, lines):
        for line in lines:
            self.write(line)


def redirectFunc(out, func, **kargs):
    stdout = sys.stdout
    sys.stdout = GuiOutput(out)
    sys.stderr = sys.stdout
    result = func(**kargs)
    sys.stdout = stdout
    return result


class BackupUI(Frame):

    dataQueue = queue.Queue()

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent)

        self.backup = None

        self.top = Frame(self)
        self.top.pack(side=TOP, expand=YES, fill=X)
        self.top.config(bd=2)
        # self.tlb = Label(self.top, text='TOP').pack(expand=YES, fill=X)

        self.login = Frame(self.top)
        self.login.config(padx=4, pady=4)
        self.login.pack(side=LEFT)
        row_names = const.LOGIN_FIELDS
        row_comments = const.LOGIN_COMMENTS

        self.inputs = []
        for i in range(3):
            lbl = Label(self.login, text=row_names[i])
            lbl.config(padx=4, pady=4)
            lbl.grid(row=i, column=0, sticky=NSEW)
            var = StringVar()
            self.inputs.append(var)
            ent = Entry(self.login, width=20, textvariable=var)
            ent.grid(row=i, column=1, sticky=NSEW)
            cmt = Label(self.login, text=row_comments[i])
            cmt.config(padx=6, pady=4, fg='red')
            cmt.grid(row=i, column=2, sticky=W)
            self.login.rowconfigure(i, weight=1)
        self.login.columnconfigure(0, weight=1)
        self.login.columnconfigure(1, weight=1)
        self.login.columnconfigure(2, weight=1)

        self.bgrp = Frame(self.top, padx=10, pady=10)
        self.bgrp.pack(side=RIGHT, expand=YES, fill=Y)
        self.btnStart = Button(self.bgrp, text='开始备份', command=self.start)
        self.btnStart.pack(side=TOP)
        self.btnStop = Button(self.bgrp, text='停止备份', command=self.stop)
        self.btnStop.pack(side=TOP)

        self.intro = Label(
            self, text=textwrap.fill(const.AUTH_DESCRIPTION, 60))
        self.intro.config(padx=8, wraplength=0)
        self.intro.config(fg='dark blue')
        self.intro.config(anchor=W, justify=LEFT)
        self.intro.pack(side=TOP, expand=YES, fill=X)

        Separator(self).pack(side=TOP)

        self.bottom = Frame(self)
        self.bottom.pack(side=BOTTOM, expand=YES, fill=X)
        self.bottom.config(bd=2)
        Label(self.bottom, text='BOTTOM').pack(expand=YES, fill=X)

        self.text = ScrolledText(self)
        self.text.pack(side=TOP, expand=YES, fill=BOTH)
        self.text.config(bg='black', fg='white')
        self.text.config(
            padx=10, pady=10, font=('Helvetica', 10, 'normal'))
        self.text.insert(END, 'This is English Text. 中文显示有没有问题。')

    def write(self, message):
        self.dataQueue.put(message)

    def updateText(self, message):
        self.text.insert(END, str(message))
        self.text.see(END)
        self.text.update()

    def updateUI(self):
        try:
            message = self.dataQueue.get(block=False)
            if message:
                self.updateText(message)
        except queue.Empty:
            pass
        self.after(200, self.updateUI)

    def stop(self):
        if getattr(self, 'backup'):
            self.backup.cancel()
        else:
            print('备份还没有开始')

    def start(self):
        keys = ['username', 'password', 'target']
        values = map(lambda x: x.get(), self.inputs)
        if not any(values):
            showerror(const.NO_INPUT_TITLE, const.NO_INPUT_MESSAGE)
        else:
            options = dict(zip(keys, values))
            # print('prepare backup options:', options)
            self.backup = tools.Backup(**options)
            reload(tools)
            threading.Thread(
                target=redirectFunc(self, self.backup.start)).start()
            self.text.delete('0.0', END)
            self.updateUI()


def _exit():
    try:
        root.quit()
        ui.stop()
    except Exception, e:
        sys.exit

if __name__ == '__main__':

    root = Tk()
    root.title('{0} v{1}'.format(const.APP_NAME, __version__))
    root.iconname(const.APP_NAME)
    # root.minsize(320, 240)
    ui = BackupUI(root)
    ui.pack()
    root.protocol('WM_DELETE_WINDOW', _exit)
    root.mainloop()
