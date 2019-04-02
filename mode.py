from model import Model
import json, wx, pdb


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
        return [str(title) for title in titles]
            
            
    def open(self, id):
        '''打开nodes记录'''
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
    
        if self.nodes:
            node = self.nodes[0]
            x, y, color = node
            return (x, y)
        
        
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        if self.id is not None:
            self.model.setfiled(self.id, pos=self.pos)
            
            
    def open(self, *args, **kwargs):
        
        super().open(*args, **kwargs)
        self.pos = self.model.getfiled('pos', id=self.id)[0][0]
        
        