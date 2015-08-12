#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 20:01:02
from __future__ import print_function
import textwrap
import sys
import os
import imp
import threading
from datetime import datetime
import Queue as queue
from Tkinter import *
from ttk import Separator
from tkFileDialog import askdirectory
from tkSimpleDialog import *
from tkMessageBox import showerror, showinfo
from ScrolledText import ScrolledText
from fanfou import const
from fanfou import backup

__version__ = const.APP_VERSION

_stdout = sys.stdout


class GuiOutput:

    def __init__(self, output):
        self.stdout = sys.stdout
        self.output = output

    def write(self, text):
        # self.stdout.write(text)
        self.output.write(text)

    def writelines(self, lines):
        for line in lines:
            self.write(line)


def redirectFunc(out, func, **kwargs):
    stdout = sys.stdout
    sys.stdout = GuiOutput(out)
    sys.stderr = sys.stdout
    result = func(**kwargs)
    sys.stdout = stdout
    return result


class BackupUI(Frame):

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, padx=10, pady=10)

        self.dataQueue = queue.Queue()
        self.thread = None
        self.outputPath = StringVar()

        self.top = Frame(self)
        self.top.pack(side=TOP, expand=YES, fill=X)
        self.top.config(bd=2)
        self.createForm()
        self.createButtons()
        self.createText()

    def createButtons(self):

        frm = Frame(self.top)
        frm.pack(side=RIGHT, expand=YES, anchor=NE)
        self.btnStart = Button(frm, text='开始备份', command=self.start)
        self.btnStart.pack(side=TOP)
        self.btnStop = Button(frm, text='停止备份', command=self.stop)
        self.btnStop.pack(side=TOP)
        self.btnStop.config(state=DISABLED)

        frm = Frame(self)
        frm.pack(side=TOP, anchor=W)
        self.btnSelect = Button(frm, text='选择保存路径', command=self.selectPath)
        self.btnSelect.pack(side=LEFT)
        self.savePath = Entry(frm, width=45, textvariable=self.outputPath)
        self.savePath.pack(side=LEFT)
        self.savePath.insert(END, os.path.expanduser('~/Documents/fanfou/'))

    def createForm(self):
        self.login = Frame(self.top)
        # self.login.config(padx=4, pady=4)
        self.login.pack(side=LEFT, anchor=W)
        fields = const.LOGIN_FIELDS

        self.inputs = []
        for i in range(len(fields)):
            lbl = Label(self.login, text=fields[i])
            lbl.grid(row=i, column=0)
            var = StringVar()
            self.inputs.append(var)
            ent = Entry(self.login, textvariable=var)
            ent.grid(row=i, column=1)
            self.login.rowconfigure(i, weight=1)
        self.login.columnconfigure(0, weight=1)
        self.login.columnconfigure(1, weight=1)

    def createText(self):
        self.content = Frame(self)
        self.content.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = ScrolledText(self.content)
        self.text.pack(side=TOP, expand=YES, fill=BOTH)
        self.text.config(bg='light gray', fg='black')
        self.text.config(
            padx=10, pady=10, font=('Helvetica', 12, 'normal'))
        self.text.insert(END, const.USER_GUIDE)
        self.text.config(state=DISABLED)

    def selectPath(self):
        path = askdirectory(initialdir='.')
        if path:
            self.savePath.delete(0, END)
            self.savePath.insert(END, path)

    def write(self, message):
        if message and message.strip():
            # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.dataQueue.put(timestamp+" - "+message+'\n')

    def updateText(self, message):
        self.text.config(state=NORMAL)
        self.text.insert(END, str(message))
        self.text.config(state=DISABLED)
        self.text.see(END)
        self.text.update()

    def updateUI(self):
        try:
            message = self.dataQueue.get(block=False)
            if message:
                self.updateText(message)
        except queue.Empty:
            pass
        running = self.thread and self.thread.is_alive()
        self.btnStart.config(state=DISABLED if running else NORMAL)
        self.btnStop.config(state=NORMAL if running else DISABLED)
        self.after(100, self.updateUI)

    def stop(self):
        if getattr(self, 'thread'):
            self.thread.stop()

    def start(self):
        keys = ['username', 'password', 'target']
        values = map(lambda x: x.get(), self.inputs)
        if not any(values):
            showerror(const.NO_INPUT_TITLE, const.NO_INPUT_MESSAGE)
            return
        options = dict(zip(keys, values))
        options['output'] = self.outputPath.get()
        print('start backup with options:', options)
        self.text.config(state=NORMAL)
        self.text.delete('0.0', END)
        self.text.config(state=DISABLED)
        self.updateUI()
        self.thread = BackupThread(self, self.dataQueue, **options)
        self.thread.start()


class BackupThread(threading.Thread):

    def __init__(self, callback, dataQueue, **options):
        super(BackupThread, self).__init__(name='BackupThread')
        imp.reload(backup)
        self.callback = callback
        self.dataQueue = dataQueue
        self.backup = backup.Backup(**options)

    def write(self, message):
        if message and message.strip():
            # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.dataQueue.put(timestamp+" - "+message+'\n')

    def stop(self):
        if getattr(self, 'backup'):
            self.backup.stop()
        else:
            print('备份还没有开始')

    def run(self):
        redirectFunc(self, self.backup.start)


def center(root):
    # https://bbs.archlinux.org/viewtopic.php?id=149559
    # Apparently a common hack to get the window size. Temporarily hide the
    # window to avoid update_idletasks() drawing the window in the wrong
    # position.
    root.withdraw()
    root.update_idletasks()  # Update "requested size" from geometry manager

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y-50))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    root.deiconify()


def start():
    root = Tk()
    root.title('{0} v{1}'.format(const.APP_NAME, __version__))
    root.iconname(const.APP_NAME)
    root.resizable(FALSE, FALSE)
    ui = BackupUI(root)
    ui.pack()
    root.protocol('WM_DELETE_WINDOW', lambda: print(
        '程序关闭') or ui.stop() or root.quit())
    center(root)
    root.mainloop()

if __name__ == '__main__':
    start()
