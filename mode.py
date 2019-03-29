from model import Model
import json, wx


class Mode():

    
    def __init__(self, table, clicked=True):
        
        self.id = None
        self.nodes = None
        self.model = Model(table)
        self.clicked = clicked
        
        
    def save(self, nodes):
        '''保存nodes记录'''
        nodes = json.dumps(nodes)
        if self.id is None:
            name = wx.GetTextFromUser(parent=None, message="请输入围棋记录名", caption="围棋记录名", default_value="")
            if name:
                self.id = self.model.insert(nodes, name)
        else:
            self.model.setfiled(self.id, 'nodes', nodes)    

    @property
    def titles(self):
        
        titles = self.model.getall('id', 'name', 'lastTime')
        return [str(title) for title in titles]
        
        
    def open(self, id):
        '''打开nodes记录'''
        self.id = id
        nodes = self.model.getfiled(self.id, 'nodes')
        self.nodes = json.loads(nodes)
        
        
    def delete(self, id):
        '''删除一行记录'''
        self.model.delete(id)
        
        