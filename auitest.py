# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:58:17 2019

@author: user
"""

import wx, pdb
import wx.lib.agw.aui as aui
from newBoard import GoBoard
from dbs import DbData


class Player():
    
    
    def __init__(self,):
        
        self.db = DbData()
        self.id = None
        self.cache = None
        
    
    @property
    def titles(self):
        
        return [str(title) for title in self.db.outTitles()]
        
    def setcache(self, id):
        
        self.cache = self.db.getRecord(id)
        self.id = id
        
        
    def save(self, nodes):
    
        if self.id is None:
            name = wx.GetTextFromUser(parent=None, message="请输入围棋记录名", caption="围棋记录名", default_value="")
            if name:
                self.id = self.db.insert(nodes, name)
        else:
            self.db.update(nodes, self.id)
    

    def deleId(self, id):
        
        self.db.delete(id)
        

class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="AUI Test", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)
        
        # 创建玩家
        self.player = Player()
        
        # 创建定时器
        self.clktime = 2000
        self.timer = wx.Timer(self)
        
        # 创建菜单
        self.createMenuBar()        
        #self.toolbar = aui.auibar.AuiToolBar(self)
        
        # 创建面板
        self.history = wx.ListBox(self, -1, choices=self.player.titles, size = wx.Size(200,150))
        self.history.SetSelection(0)
                                   
        self.board = GoBoard(wx.Image("back.png"), parent=self, style=wx.FULL_REPAINT_ON_RESIZE)
        
        self.stones = wx.ListBox(self, -1, choices=self.board.strnodes, size=wx.Size(200,150))
        
        # add the panes to the manager
        #self._mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Top())
        self._mgr.AddPane(self.history, aui.AuiPaneInfo().Left().Caption("历史记录"))
        self._mgr.AddPane(self.stones, aui.AuiPaneInfo().Right().Caption("下棋位置"))
        self._mgr.AddPane(self.board, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()
        
        #Bind event
        self.history.Bind(wx.EVT_LISTBOX, self.OnHistory)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    
    
    def OnHistory(self, event):
        
        #string = event.GetString().strip('()')
        #id = int(string.split(',')[0])
        #self.player.setcache(id)
        #print(self.player.cache)
        #pdb.set_trace()
        pass
        
    
    def OnTimer(self, event):
        
        self.placeOne()
        
        
    def OnLeftDown(self, event):
    
        self.stones.Set(self.board.strnodes)
        
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()


    def createMenuBar(self):
                
        menuMode = wx.Menu()
        startQi = menuMode.AppendRadioItem(-1, "我的棋谱")
        newQi = menuMode.AppendRadioItem(-1, "专家棋谱")
        openQi = menuMode.AppendRadioItem(-1, "定式")
        
        #self.Bind(wx.EVT_MENU, self.OnStart, startQi)
        #self.Bind(wx.EVT_MENU, self.OnNew, newQi)
        #self.Bind(wx.EVT_MENU, self.OnOpen, openQi)
        
        menuEdit = wx.Menu()
        newb = menuEdit.Append(-1, "新建")
        save = menuEdit.Append(-1, "保存")
        saveAs = menuEdit.Append(-1, "另保存")
        clea = menuEdit.Append(-1, "清理")
        daka = menuEdit.Append(-1, "打开")
        dele = menuEdit.Append(-1, "删除")
        imag = menuEdit.Append(-1, "保存图片")
        
        self.Bind(wx.EVT_MENU, self.OnNewb, newb)
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveAs)
        self.Bind(wx.EVT_MENU, self.OnDaka, daka)
        self.Bind(wx.EVT_MENU, self.OnDele, dele)
        self.Bind(wx.EVT_MENU, self.OnClea, clea)
        self.Bind(wx.EVT_MENU, self.OnImag, imag)
        
        menuClok = wx.Menu()
        quk = menuClok.Append(-1, "快速")
        man = menuClok.Append(-1, "手动")
        aut = menuClok.Append(-1, "自动")
        
        self.Bind(wx.EVT_MENU, self.OnQuk, quk)
        self.Bind(wx.EVT_MENU, self.OnMan, man)
        self.Bind(wx.EVT_MENU, self.OnAut, aut)
        
        menuSets = wx.Menu()
        num = menuSets.Append(-1, "数字的显示")
        clk = menuSets.Append(-1, "定时的时间")
        
        self.Bind(wx.EVT_MENU, self.OnNum, num)
        self.Bind(wx.EVT_MENU, self.OnClk, clk)
        
        menuBar = wx.MenuBar()        
        menuBar.Append(menuMode, "模式")
        menuBar.Append(menuEdit, "编辑")
        menuBar.Append(menuClok, "定时")
        menuBar.Append(menuSets, "设置")
        self.SetMenuBar(menuBar)
    
    def OnClk(self, event):
        
        clktime = wx.GetNumberFromUser(message='ms为单位：', prompt='', caption="定时器的间隔时间", value=self.clktime, min=0, max=60000)        
        if clktime >= 0:
            self.clktime = clktime
            if self.timer.IsRunning():
                self.timer.Start(self.clktime)
                
        
    def OnNum(self, event):
        
        self.board.toggleNumber()
        
    
    def OnQuk(self, event):
        
        self.placeAll()
    
    
    def OnMan(self, event):
        
        self.timer.Stop()
        
        
    def OnAut(self, event):
        
        self.timer.Start(self.clktime)
        
                
    def OnNewb(self, event):
        
        self.clea()
        self.player.id = None
        
        
    def OnSave(self, event):
        
        self.player.save(self.board.nodes)
        self.history.Set(self.player.titles)
    
    def OnSaveAs(self, event):
        
        self.player.id = None
        self.player.save(self.board.nodes)
        self.history.Set(self.player.titles)
        
        
    def OnClea(self, event):
        
        self.clea()
        
        
    def OnDaka(self, event):
    
        self.clea()
        self.player.setcache(self.selectedId)
        
                
    def OnDele(self, event):
    
        self.player.deleId(self.selectedId)
        self.history.Set(self.player.titles)
    
    
    def clea(self):
        
        self.board.clear()
        self.stones.Set(self.board.strnodes)
        
    def OnImag(self, event):
        
        self.board.saveImage()
        
        
    @property
    def selectedId(self):
        
        num = self.history.GetSelection()
        id = self.history.GetString(num).strip('()').split(',')[0]
        return id
        
    
    def placeOne(self):
        
        if self.player.cache:
            node = self.player.cache.pop(0)
            self.board.placeByNode(node)
            self.stones.Set(self.board.strnodes)
            
                
    def placeAll(self):
                
        while self.player.cache:
            node = self.player.cache.pop(0)
            self.board.placeByNode(node)
        self.stones.Set(self.board.strnodes)
            
            
# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()