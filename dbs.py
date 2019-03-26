# -*- coding: utf-8 -*-
import sqlite3, datetime, json


class DbData():
    
    
    def __init__(self):
        
        self.conn = sqlite3.connect("qi.db")
        self.cur = self.conn.cursor()
        self.tables = ["mine", "expert", "taolu", "sihuo"]
        self.initTable()
        self.table = "mine"
        
        
    def initTable(self):
        
        for table in self.tables:
            createTableStmt = '''create table if not exists {0}(
                        id integer primary key autoincrement,
                        name varchar(32),
                        createdTime timestamp DEFAULT (datetime('now','localtime')),
                        lastTime timestamp,
                        record varchar(4000),
                        ans integer DEFAULT NULL)'''.format(table)
            self.cur.execute(createTableStmt)
        self.conn.commit()
    
    
    def close(self):
        
        self.cur.close()
        self.conn.close()
    
    
    def __del__(self):
        
        print("close db")
        self.close()
        
        
    def insert(self, nodes, name):
        insertStmt = '''insert into {0} (lastTime, record, name)values(?, ?, ?)'''.format(self.table)
        dt = (datetime.datetime.now(), json.dumps(nodes), name)
        self.cur.execute(insertStmt, dt)
        self.conn.commit()
        return self.lastId()
    
    
    def delete(self, id):
        if id is None:
            return
        deleteStmt = '''delete from {0} where id = ?'''.format(self.table)
        self.cur.execute(deleteStmt, (id, ))
        self.conn.commit()
        
        
    def lastId(self):    
        self.cur.execute("select last_insert_rowid() from {0};".format(self.table))#cur.rowcount()
        return self.cur.fetchone()[0]
    
    
    def update(self, nodes, id):
        updateStmt = '''update {0} set lastTime = ? , record = ? where id = ?;'''.format(self.table)
        dt = (datetime.datetime.now(), json.dumps(nodes), id)
        self.cur.execute(updateStmt, dt)
        self.conn.commit()
    
    
    def setDaan(self, num, id):
        
        updateStmt = '''update {0} set ans = ? where id = ?;'''.format(self.table)        
        self.cur.execute(updateStmt, (num, id))
        self.conn.commit()
        
    
    def getDaan(self, id):
        
        Stmt = '''select ans from {0} where id = ?'''.format(self.table)
        self.cur.execute(Stmt, (id,))
        ans = self.cur.fetchone()[0]
        return int(ans)
        
        
    def outTitles(self):
        selectStmt = '''select id, name, lastTime from {0}'''.format(self.table)
        self.cur.execute(selectStmt)
        return self.cur.fetchall()    
    
    
    def getRecord(self, id):
        Stmt = '''select record from {0} where id = ?'''.format(self.table)
        self.cur.execute(Stmt, (id,))
        record = self.cur.fetchone()[0]
        return json.loads(record)  
        
        
    def out(self):
        selectStmt = '''select * from {0}'''.format(self.table)
        self.cur.execute(selectStmt)
        return self.cur.fetchall()