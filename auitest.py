# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:58:17 2019

@author: user
"""

import wx
import wx.lib.agw.aui as aui
from newBoard import GoBoard

class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="AUI Test", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create several text controls
        text1 = wx.ListBox(self, -1, choices=list("Pane 1 - sample text"),
                            size = wx.Size(200,150))

        text2 = wx.ListBox(self, -1, choices=list("Pane 2 - sample text"),
                            size=wx.Size(200,150))
                            
        board = GoBoard(wx.Image("back.png"), parent=self, style=wx.FULL_REPAINT_ON_RESIZE)
        
        # add the panes to the manager
        self._mgr.AddPane(text1, aui.AuiPaneInfo().Left().Caption("Pane Number One"))
        self._mgr.AddPane(text2, aui.AuiPaneInfo().Right().Caption("Pane Number Two"))
        self._mgr.AddPane(board, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def OnLeftDown(self, event):
        print(event)
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()