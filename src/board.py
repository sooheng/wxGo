# -*- coding: utf-8 -*-

import time

import wx

import law


def node_str(x, y, color):
    black = "●"
    white = "○"
    if color == 1:
        return ",".join((str(x + 1), str(y + 1), black))
    elif color == -1:
        return ",".join((str(x + 1), str(y + 1), white))
    else:
        raise Exception("color 只能是1或者-1")


class DataBoard(law.Board):

    def __init__(self):
        self.clear()

    def clear(self):
        super(DataBoard, self).__init__()
        self.color = 1
        self.hands = 1
        self.nodes = []

    @property
    def strnodes(self):
        """字符化nodes,用于显示"""
        return [node_str(*node) for node in self.nodes]

    def place(self, x, y, color=None):
        if color is None:
            color = self.color

        super(DataBoard, self).place(x, y, color, self.hands)

        self.hands += 1
        self.color = -self.color
        self.nodes.append((x, y, color))


# self.Refresh(False)更新画面
class GoBoard(wx.Panel):
    allPoints = [(x, y) for x in range(19) for y in range(19)]

    def __init__(self, image, dataBaord, *args, **kwargs):

        super(GoBoard, self).__init__(*args, **kwargs)

        self.xy = None
        self.data = dataBaord
        self.brush = {1: wx.Brush("Black"), -1: wx.Brush("White")}
        self.textcolor = {1: wx.Colour(0, 0, 0), -1: wx.Colour(255, 255, 255)}
        self.showNumber = True
        self.image = image
        self.calc()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

    def setShowNumber(self, shown):

        self.showNumber = shown
        self.Refresh(False)

    def calc(self):
        """控件参数的计算"""
        w, h = self.GetSize()
        s = min(w, h)
        self.gap = s // 20
        self.halfgap = self.gap // 2
        self.quartergap = self.gap // 4
        self.xgap = self.gap // 3
        self.ygap = self.gap // 3

        font = self.GetFont()
        font.SetPointSize(self.gap // 3)
        self.SetFont(font)

        self.backPhoto = self.image.Scale(s, s).ConvertToBitmap()
        dc = wx.BufferedDC(None, self.backPhoto)
        self.DrawLines(dc)
        self.DrawXin(dc)
        self.DrawText(dc)

    def DrawText(self, dc):

        pen = wx.Pen("Black")
        dc.SetPen(pen)
        for i in range(1, 20):
            dc.DrawText("{:^6d}".format(i), i * self.gap - self.halfgap, 0)
            dc.DrawText(str(i), 0, i * self.gap - self.quartergap)

    def DrawXin(self, dc):
        brush = wx.Brush("Black")
        dc.SetBrush(brush)
        for i in range(4, 19, 6):
            for j in range(4, 19, 6):
                dc.DrawCircle(self.gap * i, self.gap * j, 4)

    def DrawLines(self, dc):

        pen = wx.Pen("Black", 1)
        dc.SetPen(pen)
        for i in range(1, 20):
            dc.DrawLine(self.gap * 1, self.gap * i, self.gap * 19, self.gap * i)
            dc.DrawLine(self.gap * i, self.gap * 1, self.gap * i, self.gap * 19)

    def DrawPieces(self, dc):
        """画出所有棋子"""
        for point in self.allPoints:
            x, y = point
            piece = self.data.board[x][y]
            if piece:
                self.DrawPiece(dc, x, y, piece)

    def DrawPiece(self, dc, x, y, piece):
        """画一个棋子"""
        x, y = self.L2P(x, y)
        brush = self.brush.get(piece.color)
        if brush is not None:
            dc.SetBrush(brush)
            dc.DrawCircle(x, y, self.halfgap)

        if self.showNumber and piece.color:
            dc.SetTextForeground(self.textcolor[-piece.color])
            dc.DrawText(str(piece.hand), x - self.xgap, y - self.ygap)

    def OnPaint(self, event):
        """画图事件处理器"""
        self.buffer = wx.Bitmap(self.backPhoto)
        dc = wx.BufferedPaintDC(self, self.buffer)
        self.DrawPieces(dc)

    def L2P(self, x, y):

        calcul = lambda i: i * self.gap + self.gap
        return (calcul(x), calcul(y))

    def P2L(self, x, y):
        """pixel to logic
        点击的位置转化成围棋盘的位置"""
        calcul = lambda i: (i - self.halfgap) // self.gap
        x = calcul(x)
        if x < 0 or x > 18:
            return None
        y = calcul(y)
        if y < 0 or y > 18:
            return None
        return (x, y)

    def saveImage(self):
        """图片保存"""
        name = "screens/%s.jpg" % time.strftime("%Y%m%d%H%M%S", time.localtime())
        with open(name, "w"):
            pass
        typ = wx.BITMAP_TYPE_JPEG
        return self.buffer.SaveFile(name, typ)

    def OnLeftDown(self, event):
        """鼠标左键点击处理"""
        self.xy = self.P2L(*event.GetPosition())
        self.GetParent().OnLeftDown()

    def OnErase(self, event):
        """控件擦除处理器"""
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        dc.DrawBitmap(self.backPhoto, 0, 0)

    def OnSize(self, event):
        """控件缩放处理器"""
        self.ClearBackground()
        self.calc()
