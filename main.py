# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:58:17 2019

@author: user
"""

import wx, pdb
import wx.lib.agw.aui as aui
from board import GoBoard, DataBoard
from mode import Mode, Mode2


tb_next = wx.NewId()
me_save = wx.NewId()
me_saveAs = wx.NewId()
me_daan = wx.NewId()

dataBoard = DataBoard()

mine = Mode('mine')
expert = Mode('expert')
sihuo = Mode2('sihuo')
dingsi = Mode2('dingsi')


class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="围棋打谱", pos=wx.DefaultPosition,
                 size=(1200, 700), style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU,):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)
        
        # 创建设置
        self.mode = mine
        self.clicked = True
        
        #
        self.createIcon()
                
        # 创建定时器
        self.clktime = 2000
        self.timer = wx.Timer(self)        
        
        # 创建菜单
        self.createMenuBar()
        
        #创建状态条
        self.createStatusBar()
        
        #创建工具栏
        #self.createToolBar()      
        
        # 创建面板
        self.history = wx.ListBox(self, -1, choices=self.mode.titles, size = wx.Size(400,150))        
                                   
        self.board = GoBoard(wx.Image("back.png"), dataBoard, parent=self)#style=wx.FULL_REPAINT_ON_RESIZE)
        
        self.stones = wx.ListBox(self, -1, choices=dataBoard.strnodes, size=wx.Size(100,150))
        
        # add the panes to the manager
        #self._mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Top())
        self._mgr.AddPane(self.history, aui.AuiPaneInfo().Left().Caption("历史记录"))
        self._mgr.AddPane(self.stones, aui.AuiPaneInfo().Right().Caption("下棋位置"))
        self._mgr.AddPane(self.board, aui.AuiPaneInfo().CenterPane())
        #self._mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Top())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()
        
        #Bind event
        self.stones.Bind(wx.EVT_LISTBOX, self.OnStones)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        #不得已而为之
        self.timer2 = wx.Timer(self)
        self.timer2.Start(100)
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2)
        

#定时函数        
    def OnTimer(self, event):
        
        self.putstone()
        
        
    def OnTimer2(self, event):
        
        self.board.Refresh(False)

        
#所有的创建函数
    def createMenuBar(self):
                
        menuMode = wx.Menu()
        mine = menuMode.AppendRadioItem(-1, "我的棋谱")
        expert = menuMode.AppendRadioItem(-1, "职业棋谱")
        dingsi = menuMode.AppendRadioItem(-1, "定式题")
        sihuo = menuMode.AppendRadioItem(-1, "死活题")
        
        self.Bind(wx.EVT_MENU, self.OnMine, mine)
        self.Bind(wx.EVT_MENU, self.OnExpert, expert)
        self.Bind(wx.EVT_MENU, self.OnDingsi, dingsi)
        self.Bind(wx.EVT_MENU, self.OnSihuo, sihuo)
        
        menuEdit = wx.Menu()
        newb = menuEdit.Append(-1, "新建")        
        daka = menuEdit.Append(-1, "打开")
        dele = menuEdit.Append(-1, "删除")
        clea = menuEdit.Append(-1, "重新")
        save = menuEdit.Append(me_save, "保存")
        saveAs = menuEdit.Append(me_saveAs, "另存为")
                
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
        num = menuSets.AppendCheckItem(-1, "显示数字")
        num.Check(True)
        resetHistory = menuSets.Append(-1, "显示历史记录")
        resetStones = menuSets.Append(-1, "显示下棋位置")        
        
        self.Bind(wx.EVT_MENU, self.OnNum, num)                
        self.Bind(wx.EVT_MENU, self.OnResetHistory, resetHistory)
        self.Bind(wx.EVT_MENU, self.OnResetStones, resetStones)
        
        menuOutIn = wx.Menu()
        imag = menuOutIn.Append(-1, "保存图片")
        outsgf = menuOutIn.Append(-1, "导出sgf文件")
        insgf = menuOutIn.Append(-1, "读取sgf文件")
        insgfs = menuOutIn.Append(-1, "读取sgf文件目录")
        
        self.Bind(wx.EVT_MENU, self.OnImag, imag)
        self.Bind(wx.EVT_MENU, self.OnOutsgf, outsgf)
        self.Bind(wx.EVT_MENU, self.OnInsgf, insgf)
        self.Bind(wx.EVT_MENU, self.OnInsgfs, insgfs)
        
        menuOthers = wx.Menu()
        tip = menuOthers.Append(-1, "提示")        
        daan = menuOthers.Append(me_daan, "插入断点")
        
        self.Bind(wx.EVT_MENU, self.OnTip, tip)        
        self.Bind(wx.EVT_MENU, self.OnPos, daan)
        
        menuAbout = wx.Menu()
                
        menuBar = wx.MenuBar()        
        menuBar.Append(menuMode, "模式")
        menuBar.Append(menuEdit, "编辑")
        menuBar.Append(menuClok, "定时")
        menuBar.Append(menuSets, "设置")
        menuBar.Append(menuOthers, "其他")
        menuBar.Append(menuAbout, "关于")
        self.SetMenuBar(menuBar)
        
        
    def createIcon(self):
        '''设置图标'''
        icon = wx.Icon(name='图标.jpg', type=wx.BITMAP_TYPE_JPEG)
        self.SetIcon(icon)        
        
                
    def createToolBar(self):
        
        self.toolbar = wx.ToolBar(self, -1)
        self.toolbar.AddTool(tb_next, "next", wx.Bitmap("ps.png"))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnNext, id=tb_next)
        self.toolbar.Realize()
        
        
    def createStatusBar(self):
        
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(4)
        self.statusBar.SetStatusWidths([-1,-1,-3,-3])
        self.statusBar.SetStatusText("可编辑：", 0)
        self.statusBar.SetStatusText(str(self.clicked), 1)
        
    
    def OnResetHistory(self, event):
        '''重新显示历史记录'''
        pane = self._mgr.GetPane(self.history)
        if not pane.IsShown():
            pane.Show()
            self._mgr.Update()
    

    def OnResetStones(self, event):
        '''重新显示下棋位置'''
        pane = self._mgr.GetPane(self.stones)
        if not pane.IsShown():
            pane.Show()
            self._mgr.Update()
        
        
    def OnStones(self, event):
        
        num = self.stones.GetSelection() + 1
        if self.mode.id is None:
            self.mode.nodes = dataBoard.nodes[:num]
        else:
            self.mode.open()
        dataBoard.clear()
        self.putstone(num)        
        
    
    def OnNext(self, event):
        
        self.clicked = not self.clicked
        self.statusBar.SetStatusText(str(self.clicked), 1)
        
        
    def OnLeftDown(self):
                
        if self.clicked and self.board.xy and dataBoard.canPlace(*self.board.xy):
            #编辑写入
            dataBoard.place(*self.board.xy)
            self.stones.Set(dataBoard.strnodes)
            self.board.Refresh(False)
            statusText = str(self.board.xy)
            self.board.xy = None
        else:
            #只可以读取
            if self.mode in (mine, expert):
                self.putstone()
                statusText = str(dataBoard.hands)
            else:
                if self.mode.curentxy == self.board.xy:
                    if self.mode is dingsi:
                        self.putstone()
                    else:
                        self.putstone(2)
                    statusText = "正确的位置"
                else:
                    statusText = "错误的位置"        
        self.statusBar.SetStatusText(statusText, 2)
        
        
    
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
                        
        
    def _change_mode(self, mode, enableClock=True):
        
        self.mode = mode
        menuBar = self.GetMenuBar()
        menuBar.EnableTop(2, enableClock)
        self.history.Set(self.mode.titles)        
        
        



    def OnTip(self, event):
        
        wx.MessageBox(str(self.mode.nodes), caption="围棋记录", style=wx.OK)
        
        
    def OnClk(self, event):
        '''定时的时间设置事件处理'''
        clktime = wx.GetNumberFromUser(message='ms为单位：', prompt='', caption="定时器的间隔时间", value=self.clktime, min=0, max=60000)        
        if clktime >= 0:
            self.clktime = clktime
            if self.timer.IsRunning():
                self.timer.Start(self.clktime)
                
        
    def OnNum(self, event):
        
        self.board.setShowNumber(event.IsChecked())
        
    
    def OnQuk(self, event):
        
        self.putstone(-1)
    
    
    def OnMan(self, event):
        
        self.timer.Stop()        
        
        
    def OnAut(self, event):
        
        self.timer.Start(self.clktime)
        
                
    def OnNewb(self, event):
        '''新建操作处理'''
        self.clea()
        self.mode.id = None
        self.clicked = True
        self.statusBar.SetStatusText(str(self.clicked), 1)
        
    def OnSave(self, event):
        '''保存事件处理'''
        self.mode.save(dataBoard.nodes)
        self.history.Set(self.mode.titles)        
        
    
    def OnSaveAs(self, event):
        
        self.mode.id = None
        self.OnSave(event)              
        
        
    def OnPos(self, event):
    
        num = wx.GetNumberFromUser(message='', prompt='', caption="插入的断点", value=0, min=0, max=len(dataBoard.nodes))
        if num != -1:
            self.mode.pos = num
        
        
    def OnClea(self, event):
        '''重新事件处理'''
        self.clea()
        
        
    def OnDaka(self, event):
        '''打开事件处理'''
        self.clea()
        self.clicked = False
        self.statusBar.SetStatusText(str(self.clicked), 1)
        self.mode.open(self.selectedId)
        if hasattr(self.mode, 'pos'):
            self.putstone(self.mode.pos)
        
                
    def OnDele(self, event):
        '''删除事件处理'''
        self.mode.delete(self.selectedId)
        self.history.Set(self.mode.titles)
    
    
    def clea(self):
        '''清空棋盘'''
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
                          
    
    def putstone(self, num=1):
        '''num 落子的数目，负数表示全部下完'''
        if num < 0:
            while self.mode.nodes:
                node = self.mode.nodes.pop(0)
                dataBoard.place(*node)
        else:
            for i in range(num):
                if self.mode.nodes:
                    node = self.mode.nodes.pop(0)
                    dataBoard.place(*node)
                else:
                    break                    
        self.board.Refresh(False)
        self.stones.Set(dataBoard.strnodes)            
                                  
            
# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()