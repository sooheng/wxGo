# -*- coding: utf-8 -*-

import wx
from src import MyFrame, CreateTables


def is_exe_running():
    """ 当前程序在正常运行，而不是在py2exe打包模式下 """
    return True
    #import os.path
    #cwd = os.getcwd()
    #return not os.path.isdir("./src")


# our normal wxApp-derived class, as usual
if __name__ == "__main__":
    if is_exe_running():
        CreateTables()

    app = wx.App(0)
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
