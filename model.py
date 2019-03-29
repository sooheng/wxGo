import sqlite3, datetime


class Model():
    '''数据库接口类'''
    __conn = sqlite3.connect("weiqi.db")
    selectSt = '''select {field} from {table} where id = {id}'''
    updateSt = '''update {table} set {field} = {vaule} where id = {id}'''
    insertSt = '''insert into {table} (lastTime, nodes, name)values(?, ?, ?)'''
    deleteSt = '''delete from {table} where id = {id}'''
    selectAllSt = '''select {fields} from {table}'''
    
    def __init__(self, table):
        '''创建游标、表'''
        self.__table = table
        self.cur = self.__conn.cursor()
        self.__createTable()
        
        
    def __createTable(self):
        '''如果表不存在的话，创建表'''
        createTableStmt = '''create table if not exists {0}(
                        id integer primary key autoincrement,
                        name varchar(32),
                        createdTime timestamp DEFAULT (datetime('now','localtime')),
                        lastTime timestamp,
                        nodes varchar(4000),
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
        st = self.deleteSt.format(table=self.__table, id=id)
        self.cur.execute(st)
        self.__conn.commit()
        
        
    def setfiled(self, id, name, vaule):
        '''给一行记录的字段赋值
        id : 记录的主键
        name : 记录的字段
        vaule : 字段的值'''
        st = self.updateSt.format(field=name, table=self.__table, vaule=vaule, id=id)
        self.cur.execute(st)
        st = self.updateSt.format(field='lastTime', table=self.__table, vaule=datetime.datetime.now(), id=id)
        self.cur.execute(st)
        self.__conn.commit()
        
    
    def getfiled(self, id, name):
        '''获得一行记录的字段的值
        id : 数据库的主键
        name : 记录的字段'''
        st = self.selectSt.format(field=name, table=self.__table, id=id)
        self.cur.execute(st)
        row = self.cur.fetchone()
        return row[0]
        
    
    def getall(self, *names):
        '''获得所有记录的一些字段值
        names : 字段名'''
        fields = ','.join(names)
        st = self.selectAllSt.format(fields=fields, table=self.__table)
        self.cur.execute(st)
        rows = self.cur.fetchall()
        return rows
        
        
    def __del__(self):
        '''关闭游标'''
        self.cur.close()


def __test__():
    '''测试函数'''
    import json
    model = Model('test')
    nodes = json.dumps([(1,2,3),(4,5,6)])
    print(model.insert(nodes, 'test'))
    print(model.getall('*'))
    print(model.getfiled(2, 'nodes'))
    #print(model.delete(1))
    
    

if __name__ == '__main__':
    __test__()