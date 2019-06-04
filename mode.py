from model import Model
import wx


class Mode():

    
    def __init__(self, table):
        
        self.id = None
        self.nodes = None
        self.model = Model(table)        
        
        
    def save(self, nodes):
        '''保存nodes记录'''
        if self.id is None:
            name = wx.GetTextFromUser(parent=None, message="请输入围棋记录名", caption="围棋记录名", default_value="")
            if name:
                self.id = self.model.insert(nodes, name)
        else:
            self.model.setfiled(self.id, nodes=nodes)    

    @property
    def titles(self):
        '''记录标题'''
        titles = self.model.getfiled('id', 'name', 'lastTime')
        _str = lambda id,name,lastTime : str(id) + ',' + name + ',' + str(lastTime)        
        return [_str(*title) for title in titles]
            
    
    @property
    def title(self):
        '''记录名'''
        title = self.model.getfiled('name', id=self.id)
        return title[0][0]
    
                
    def open(self, id=None):
        '''打开nodes记录'''
        if id is not None:
            self.id = id
        self.nodes = self.model.getfiled('nodes', id=self.id)[0][0]        
        
        
    def delete(self, id):
        '''删除一行记录'''
        self.model.delete(id)
        
        
class Mode2(Mode):
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.pos = 0
        
        
    @property
    def curentxy(self):
        '''返回缓存nodes里最新的一个棋子的坐标'''
        if self.nodes:
            node = self.nodes[0]
            x, y, color = node
            return (x, y)
        
        
    def save(self, *args, **kwargs):
        '''保存函数'''
        super().save(*args, **kwargs)
        if self.id is not None:
            self.model.setfiled(self.id, pos=self.pos)
            
            
    def open(self, *args, **kwargs):
        '''打开方法'''
        super().open(*args, **kwargs)
        self.pos = self.model.getfiled('pos', id=self.id)[0][0]
        
        