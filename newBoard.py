import wx, law, dbs, pdb


class DataBoard(law.Board):

    
    def __init__(self):

        self.initData()
        
    def initData(self):
        
        super().__init__()
        self.color = 1
        self.hands = 1
        
        self.db = dbs.DbData()
        self.nodes = []
        self.id = None
        
        
    def place(self, x, y, color=None):
        
        if color is None:
            color = self.color
            self.color = -self.color
            
        super().place(x, y, color, self.hands)        
        self.hands += 1
        
        self.nodes.append((x,y,color))
        
        
    def save(self, name):
        
        return self.db.insert(self.nodes, name)
        
        
    def getCacheNodes(self):
        
        return self.db.getRecord(self.id)


class GoBoard(wx.Window, DataBoard):
    
    
    allPoints = [(x,y) for x in range(19) for y in range(19)]
    
    
    def __init__(self, image, *args, **kwargs):
    
        wx.Window.__init__(self, *args, **kwargs)
        DataBoard.__init__(self)
        
        self.brush = {1 : wx.Brush("Black"), -1 : wx.Brush("White")}
        self.image = image       
        self.calc()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        
    def calc(self):
        
        w, h = self.GetSize()
        s = min(w, h)
        self.gap = s // 20
        self.halfgap = self.gap // 2
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
        
        dc.SetBrush(self.brush[piece.color])
        dc.DrawCircle(*self.L2P(x,y), self.halfgap)
        
        
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
        
        
    def OnLeftDown(self, event):
        
        xy = self.P2L(*event.GetPosition())
        if xy is None:
            return
        if self.canPlace(*xy):
            self.place(*xy)
            self.Refresh(False)
    
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
                
        