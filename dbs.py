# -*- coding: utf-8 -*-
import sqlite3, datetime, json


class DbData():
    
    
    def __init__(self):
        
        self.conn = sqlite3.connect("qi.db")
        self.cur = self.conn.cursor()
        self.open()
        
        
    def open(self):
        createTableStmt = '''create table if not exists qipu(
                    id integer primary key autoincrement,
                    name varchar(32),
                    createdTime timestamp DEFAULT (datetime('now','localtime')),
                    lastTime timestamp,
                    record varchar(4000))'''
        self.cur.execute(createTableStmt)
        self.conn.commit()
    
    
    def close(self):
        
        self.cur.close()
        self.conn.close()
    
    
    def __del__(self):
        
        print("close db")
        self.close()
        
        
    def insert(self, nodes, name):
        insertStmt = '''insert into qipu (lastTime, record, name)values(?, ?, ?)'''
        dt = (datetime.datetime.now(), json.dumps(nodes), name)
        self.cur.execute(insertStmt, dt)
        self.conn.commit()
        return self.lastId()
    
    
    def delete(self, id):
        if id is None:
            return
        deleteStmt = '''delete from qipu where id = ?'''
        self.cur.execute(deleteStmt, (id, ))
        self.conn.commit()
        
        
    def lastId(self):    
        self.cur.execute("select last_insert_rowid() from qipu;")#cur.rowcount()
        return self.cur.fetchone()[0]
    
    
    def update(self, nodes, id):
        updateStmt = '''update qipu set lastTime = ? , record = ? where id = ?;'''
        dt = (datetime.datetime.now(), json.dumps(nodes), id)
        self.cur.execute(updateStmt, dt)
        self.conn.commit()
    
    
    def outTitles(self):
        selectStmt = '''select id, name, lastTime from qipu'''
        self.cur.execute(selectStmt)
        return self.cur.fetchall()    
    
    
    def getRecord(self, id):
        Stmt = '''select record from qipu where id = ?'''
        self.cur.execute(Stmt, (id,))
        record = self.cur.fetchone()[0]
        return json.loads(record)  
        
        
    def out(self):
        selectStmt = '''select * from qipu'''
        self.cur.execute(selectStmt)
        return self.cur.fetchall()