import wx, law, dbs, time, pdb


class DataBoard(law.Board):

    
    def __init__(self):
        
        super().__init__()
        self.color = 1
        self.hands = 1
        
        self.nodes = []

        
    @property    
    def strnodes(self):
        '''字符化nodes,用于显示'''
        return [str(node) for node in self.nodes]
        
        
    def place(self, x, y, color=None):
        
        if color is None:
            color = self.color
            self.color = -self.color
            
        super().place(x, y, color, self.hands)        
        self.hands += 1
        
        self.nodes.append((x,y,color))



class GoBoard(wx.Window, DataBoard):
    
    
    allPoints = [(x,y) for x in range(19) for y in range(19)]
    
    
    def __init__(self, image, *args, **kwargs):
    
        wx.Window.__init__(self, *args, **kwargs)
        DataBoard.__init__(self)
        
        self.brush = {1 : wx.Brush("Black"), -1 : wx.Brush("White")}
        self.textcolor = {1 : wx.Colour(0, 0, 0), -1 : wx.Colour(255, 255, 255)}
        self.hasNumber = True
        self.image = image       
        self.calc()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        
    def clear(self):
        
        DataBoard.__init__(self)
        self.Refresh(False)
        
    def toggleNumber(self):
        
        self.hasNumber = not self.hasNumber
        self.Refresh(False)
        
        
    def calc(self):
        
        w, h = self.GetSize()
        s = min(w, h)
        self.gap = s // 20
        self.halfgap = self.gap // 2
        self.xgap = self.gap // 3
        self.ygap = self.gap // 3
        
        font = self.GetFont()
        font.SetPointSize(self.gap // 3)
        self.SetFont(font)
        
        self.backPhoto = self.image.Scale(s, s).ConvertToBitmap() 
        dc = wx.BufferedDC(None, self.backPhoto)
        self.DrawLines(dc)
        self.DrawXin(dc)
        
                
    def DrawXin(self, dc):
        brush = wx.Brush("Black")
        dc.SetBrush(brush)
        for i in range(4, 19, 3):
            for j in range(4, 19, 3):
                dc.DrawCircle(self.gap*i, self.gap*j, 4)
    
    
    def DrawLines(self, dc):
    
        pen = wx.Pen("Black", 1)
        dc.SetPen(pen)
        for i in range(1,20):
            dc.DrawLine(self.gap*1, self.gap*i, self.gap*19, self.gap*i)
            dc.DrawLine(self.gap*i, self.gap*1, self.gap*i, self.gap*19)
    
    
    def DrawPieces(self, dc):
        
        for point in self.allPoints:
            x, y = point
            piece = self.board[x][y]
            if piece:
                self.DrawPiece(dc, x, y, piece)
                
        
    def DrawPiece(self, dc, x, y, piece):
        
        x, y = self.L2P(x,y)
        
        dc.SetBrush(self.brush[piece.color])
        dc.DrawCircle(x, y, self.halfgap)
        
        if self.hasNumber:
            dc.SetTextForeground(self.textcolor[-piece.color])
            dc.DrawText(str(piece.hand), x-self.xgap, y-self.ygap)
        
        
    def OnPaint(self, event):
        
        self.buffer = wx.Bitmap(self.backPhoto)
        dc = wx.BufferedPaintDC(self, self.buffer)
        self.DrawPieces(dc)
        
        
    def L2P(self, x, y):
    
        calcul = lambda i : i * self.gap + self.gap
        return (calcul(x), calcul(y))
        
        
    def P2L(self, x, y):
        
        calcul = lambda i : (i - self.halfgap) // self.gap
        x = calcul(x)
        if x < 0 or x > 18:
            return None
        y = calcul(y)
        if y < 0 or y > 18:
            return None
        return (x, y)
        
    
    def saveImage(self):
    
        name = time.strftime('%Y%m%d%H%M%S',time.localtime()) + ".jpg"
        with open(name, 'w'):
            pass
        typ = wx.BITMAP_TYPE_JPEG
        return self.buffer.SaveFile(name, typ)
    
    
    def placeByNode(self, node):
        
        self.place(*node)
        self.Refresh(False)
    
    
    def OnLeftDown(self, event):
        
        xy = self.P2L(*event.GetPosition())
        if xy is None:
            return
        if self.canPlace(*xy):
            self.place(*xy)
            self.Refresh(False)
        wx.PostEvent(self.GetParent(), event)

        
    def OnErase(self, event):
        
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        dc.DrawBitmap(self.backPhoto, 0, 0) 
    
    
    def OnSize(self, event):
        
        self.ClearBackground()
        self.calc()
                
        