# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:58:17 2019

@author: user
"""

import wx, pdb
import wx.lib.agw.aui as aui
from board import GoBoard, DataBoard
from mode import Mode


tb_next = wx.NewId()
me_save = wx.NewId()
me_saveAs = wx.NewId()
me_daan = wx.NewId()

dataBoard = DataBoard()

mine = Mode('mine')
expert = Mode('expert')
sihuo = Mode('sihuo')
dingsi = Mode('dingsi')


class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="AUI Test", pos=wx.DefaultPosition,
                 size=(900, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)
        
        # 创建设置
        self.mode = mine
        
        # 创建定时器
        self.clktime = 2000
        self.timer = wx.Timer(self)
        
        # 创建菜单
        self.createMenuBar()
        
        #创建工具栏
        self.toolbar = wx.ToolBar(self, -1)
        self.toolbar.AddTool(tb_next, "next", wx.Bitmap("ps.png"))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnNext, id=tb_next)
        self.toolbar.Realize()
        
        # 创建面板
        self.history = wx.ListBox(self, -1, choices=self.mode.titles, size = wx.Size(400,150))        
                                   
        self.board = GoBoard(wx.Image("back.png"), dataBoard, parent=self, style=wx.FULL_REPAINT_ON_RESIZE)
        
        self.stones = wx.ListBox(self, -1, choices=dataBoard.strnodes, size=wx.Size(100,150))
        
        # add the panes to the manager
        #self._mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Top())
        self._mgr.AddPane(self.history, aui.AuiPaneInfo().Left().Caption("历史记录"))
        self._mgr.AddPane(self.stones, aui.AuiPaneInfo().Right().Caption("下棋位置"))
        self._mgr.AddPane(self.board, aui.AuiPaneInfo().CenterPane())
        self._mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Top())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()
        
        #Bind event
        self.history.Bind(wx.EVT_LISTBOX, self.OnHistory)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    
    
    def OnHistory(self, event):
        
        pass
        
    
    def OnTimer(self, event):
        
        self.placeOne()
        
    
    def OnNext(self, event):
        
        self.placeOne()
        
        
    def OnLeftDown(self, event):
    
        dataBoard.place(*self.board.xy)
        self.board.Refresh(False)
        self.stones.Set(dataBoard.strnodes)
        
    
    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()

    
    def OnMine(self, event):
        
        self._change_mode(mine)
        
        
    def OnExpert(self, event):
        
        self._change_mode(expert)      
        

    def OnDingsi(self, event):
        
        self._change_mode(dingsi, False)        
                
    
    def OnSihuo(self, event):
        
        self._change_mode(sihuo, False)
                        
        
    def _change_mode(self, mode, clock=True):
        
        self.mode = mode
        menuBar = self.GetMenuBar()
        menuBar.EnableTop(2, clock)
        self.history.Set(self.mode.titles)        
        
        
    def createMenuBar(self):
                
        menuMode = wx.Menu()
        mine = menuMode.AppendRadioItem(-1, "我的棋谱")
        expert = menuMode.AppendRadioItem(-1, "专家棋谱")
        dingsi = menuMode.AppendRadioItem(-1, "定式题")
        sihuo = menuMode.AppendRadioItem(-1, "死活题")
        
        self.Bind(wx.EVT_MENU, self.OnMine, mine)
        self.Bind(wx.EVT_MENU, self.OnExpert, expert)
        self.Bind(wx.EVT_MENU, self.OnDingsi, dingsi)
        self.Bind(wx.EVT_MENU, self.OnSihuo, sihuo)
        
        menuEdit = wx.Menu()
        newb = menuEdit.Append(-1, "新建")
        save = menuEdit.Append(me_save, "保存")
        saveAs = menuEdit.Append(me_saveAs, "另存为")
        daan = menuEdit.Append(me_daan, "插入答案")
        daka = menuEdit.Append(-1, "打开")
        dele = menuEdit.Append(-1, "删除")
        clea = menuEdit.Append(-1, "重新")        
        
        self.Bind(wx.EVT_MENU, self.OnDaan, daan)
        self.Bind(wx.EVT_MENU, self.OnNewb, newb)
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveAs)
        self.Bind(wx.EVT_MENU, self.OnDaka, daka)
        self.Bind(wx.EVT_MENU, self.OnDele, dele)
        self.Bind(wx.EVT_MENU, self.OnClea, clea)        
        
        menuClok = wx.Menu()
        man = menuClok.Append(-1, "手动")                
        aut = menuClok.Append(-1, "自动")
        quk = menuClok.Append(-1, "快速")
        clk = menuClok.Append(-1, "定时的时间")
        
        self.Bind(wx.EVT_MENU, self.OnQuk, quk)
        self.Bind(wx.EVT_MENU, self.OnMan, man)
        self.Bind(wx.EVT_MENU, self.OnAut, aut)
        self.Bind(wx.EVT_MENU, self.OnClk, clk)
        
        menuSets = wx.Menu()
        num = menuSets.Append(-1, "数字的显示")        
        tip = menuSets.Append(-1, "提示")
        imag = menuSets.Append(-1, "保存图片")        
        
        self.Bind(wx.EVT_MENU, self.OnNum, num)        
        self.Bind(wx.EVT_MENU, self.OnTip, tip)
        self.Bind(wx.EVT_MENU, self.OnImag, imag)
        
        menuBar = wx.MenuBar()        
        menuBar.Append(menuMode, "模式")
        menuBar.Append(menuEdit, "编辑")
        menuBar.Append(menuClok, "定时")
        menuBar.Append(menuSets, "其他")
        self.SetMenuBar(menuBar)


    def OnTip(self, event):
        
        wx.MessageBox(str(self.mode.nodes), caption="围棋记录", style=wx.OK)
        
        
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
        self.mode.id = None
        self.mode.clicked = True
        
        
    def OnSave(self, event):
        
        self.mode.save(dataBoard.nodes)
        self.history.Set(self.mode.titles)        
        
    
    def OnSaveAs(self, event):
        
        self.mode.id = None
        self.mode.save(dataBoard.nodes)
        self.history.Set(self.mode.titles)        
        
        
    def OnDaan(self, event):
        
        self.mode.saveDaan(len(dataBoard.nodes))
        
        
    def OnClea(self, event):
        
        self.clea()
        
        
    def OnDaka(self, event):
    
        self.clea()
        self.mode.open(self.selectedId)        
        
                
    def OnDele(self, event):
    
        self.mode.delete(self.selectedId)
        self.history.Set(self.mode.titles)
    
    
    def clea(self):
        
        dataBoard.clear()
        self.board.Refresh(False)
        self.stones.Set(dataBoard.strnodes)
        
        
    def OnImag(self, event):
        
        self.board.saveImage()
        
        
    @property
    def selectedId(self):
        
        num = self.history.GetSelection()
        id = self.history.GetString(num).strip('()').split(',')[0]
        return id
                          
    
    def placeOne(self):
        
        if self.mode.nodes:
            node = self.mode.nodes.pop(0)
            dataBoard.place(*node)
            self.board.Refresh(False)
            self.stones.Set(dataBoard.strnodes)
            
    
    def placeSome(self, num):
        
        for i in range(num):
            node = self.mode.nodes.pop(0)
            dataBoard.place(*node)
        self.board.Refresh(False)
        self.stones.Set(dataBoard.strnodes)
        
        
    def placeAll(self):
                
        while self.mode.nodes:
            node = self.mode.nodes.pop(0)
            dataBoard.place(*node)
        self.board.Refresh(False)
        self.stones.Set(dataBoard.strnodes)
            
            
# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()