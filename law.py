# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:12:00 2019

@author: user
"""

size = 19


class Piece():
    
    __slots__ = ("color", "hand")
    
    def __init__(self, color, hand):
        '''color: Black is 1 , White is -1
        hand: is a int number
        '''
        self.color = color
        self.hand = hand
        
    def __repr__(self):
        
        return str(self.color) + str(self.hand)
    
    def __bool__(self):
        
        if self.color is None or self.hand is None:
            return False
        else:
            return True
        

#None 表示 棋盘空位    
NonePiece = Piece(None, None)

class Jie():
    
    def __init__(self):
        
        self.hasvalue = False
        
    def __bool__(self):
        
        return self.hasvalue
    
    def __get__(self, instance, owner):
        
        if self.hasvalue:
            self.hasvalue = False
            return self.value
        else:
            raise Exception("NO VALUE")
    
    def __set__(self, instance, value):
        
        self.hasvalue = True
        self.value = value


class Board():
    
    def __init__(self):
        self.board = [[NonePiece,] * size for i in range(size)]
        self.blocks = []
        self.jiejin = None
    
    @staticmethod
    def aroundPieces(x, y):
        '''返回x, y的上下左右棋子坐标'''
        around = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        filter_around = [(xy[0],xy[1]) for xy in around if xy[0]>=0 and xy[0]<=18 and xy[1]>=0 and xy[1]<=18]
        return filter_around
    
    def sameColorPieces(self, x, y, color):
        '''返回 x, y 周围同色的棋子'''
        around = self.aroundPieces(x, y)
        ret = [xy for xy in around if self.board[xy[0]][xy[1]].color == color]
        return ret
    
    
    def hasQi(self, x, y):
        '''判断棋子x, y 有没有气'''
        around = self.aroundPieces(x, y)
        for piece in around:
            x, y = piece
            if not self.board[x][y]:
                return True
        return False
    
    def canPlace(self, x, y):
        
        if self.jiejin == (x, y):
            return False
            
        if self.board[x][y]:
            return False
        
        return True
            
    
    def place(self, x, y, color, hand):
                
        if self.jiejin:
            self.jiejin = None
        self.board[x][y] = Piece(color, hand)
        self.addIntoBlock(x, y, color)
        self.checkBlocks(-color)
        self.removeDeathBlocks()
        self.checkBlocks(color)
        self.removeDeathBlocks()

        
    def checkBlock(self, block):
        '''检查一块有没有气'''
        for piece in block:
            x, y = piece
            if self.hasQi(x, y):
                return True
        return False
    
    
    def checkBlocks(self, color):
        '''检查黑或白块有没有气'''
        for block in (block for block in self.blocks if block.color == color):
            if not self.checkBlock(block):
                block.isLive = False
                
    
    def removeDeathBlocks(self):
        '''移除没气的块'''
        for i in range(len(self.blocks)):
            if not self.blocks[i].isLive:
                for piece in self.blocks[i]:
                    x, y = piece
                    self.board[x][y] = NonePiece
                if len(self.blocks[i]) == 1:
                    self.jiejin = (x, y)
                self.blocks[i] = None
        self.blocks = list(filter(None, self.blocks))
        
            
    def addIntoBlock(self, x, y, color):
        '''棋子加入块'''
        sameColor = self.sameColorPieces(x, y, color)
        if len(sameColor) == 0:
            self.blocks.append(Block([(x, y)], color))
        else:
            temp_blocks = []
            #找到 x, y 的相邻同色块.块记录到temp_blocks。
            for i in range(len(self.blocks)):
                for xy in sameColor:
                    if xy in self.blocks[i]:
                        temp_blocks.append(self.blocks[i])
                        self.blocks[i] = None
                        break                
            #从blocks去掉所有相邻同色块
            self.blocks = list(filter(None, self.blocks))
            #合并相邻同色块到temp_block
            temp_block = Block([], color)
            temp_block = sum(temp_blocks, temp_block)
            #向temp_block加入(x,y)
            temp_block.append(x, y)
            #向blocks加入最终合并的块
            self.blocks.append(temp_block)
    
    def __repr__(self):
        
        return str(self.blocks)


class Block():
    
    def __init__(self, pieces, color):
        
        self.pieces = pieces
        self.color = color
        self.isLive = True
        
    def append(self, x, y):
        
        self.pieces.append((x, y))
        
    def __add__(self, other):
        
        self.pieces += other.pieces
        return self
    
    def __len__(self):
        
        return len(self.pieces)
    
    def __iter__(self):
        
        return iter(self.pieces)
    
    def __repr__(self):
        
        return str(self.pieces) + str(self.isLive)
    
    def __contains__(self, item):
        
        for piece in self.pieces:
            if item == piece:
                return True
        return False
    

    
        