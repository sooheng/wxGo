import sqlite3, datetime, json
    
    
    
sqlite3.register_adapter(list, json.dumps)

sqlite3.register_converter('list', json.loads)

    

class Model():
    '''数据库接口类'''
    __conn = sqlite3.connect("weiqi.db", detect_types=sqlite3.PARSE_DECLTYPES)
    selectSt = '''select {fields} from {table} where id = ?'''
    updateSt = '''update {table} set {fields} = ? where id = ?'''
    insertSt = '''insert into {table} (lastTime, nodes, name)values(?, ?, ?)'''
    deleteSt = '''delete from {table} where id = ?'''
    selectAllSt = '''select {fields} from {table}'''
    
    
    def __init__(self, table):
        '''创建游标、表'''
        self.__table = table
        self.cur = self.__conn.cursor()
        self.__createTable()
        
        
    def __createTable(self):
        '''如果表不存在的话，创建表'''
        createTableStmt = '''create table if not exists {}(
                        id integer primary key autoincrement,
                        name varchar(32),
                        createdTime timestamp DEFAULT (datetime('now','localtime')),
                        lastTime timestamp,
                        nodes list,
                        pos integer DEFAULT NULL)'''.format(self.__table)                                
        self.cur.execute(createTableStmt)
        self.__conn.commit()
        
    
    def insert(self, nodes, name):
        '''新建一行记录'''       
        st = self.insertSt.format(table=self.__table)		
        dt = (datetime.datetime.now(), nodes, name)
        self.cur.execute(st, dt)
        self.__conn.commit()
        return self.cur.lastrowid
        
    
    def delete(self, id):
        '''删除一行记录
        id : 记录的主键'''
        st = self.deleteSt.format(table=self.__table) 
        dt= (id,)
        self.cur.execute(st, dt)
        self.__conn.commit()
        
        
    def setfiled(self, id, **kwargs):
        '''给一行记录的字段赋值
        id : 记录的主键'''        
        fields = ' = ?, '.join(kwargs.keys())                
        st = self.updateSt.format(table=self.__table, fields=fields)
        dt = tuple(kwargs.values()) + (id,)
        self.cur.execute(st, dt)        
        self.__conn.commit()
        
    
    def getfiled(self, *names, id=None):
        '''获得一行记录的字段的值
        id : 数据库的主键
        names : 字段名'''
        if id is None:
            st = self.selectAllSt
            dt = ()
        else:
            st = self.selectSt
            dt = (id,)
        fields = ','.join(names)
        st = st.format(table=self.__table, fields=fields)
        self.cur.execute(st, dt)
        rows = self.cur.fetchall()
        return rows
        
        
    def __del__(self):
        '''关闭游标'''
        self.cur.close()


def __test__():
    '''测试函数'''
    import pdb
    model = Model('test')
    nodes = [(1,2,3),(4,5,6)]
    pdb.set_trace()
    #print(model.insert(nodes, 'test'))
    #print(model.getfiled('nodes'))
    #print(model.delete(1))
    
    

if __name__ == '__main__':
    __test__()