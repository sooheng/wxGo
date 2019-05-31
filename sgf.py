import re, os, shutil
from model import Model



expert = Model('expert')

trantab = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
 'p': 15, 'q': 16, 'r': 17, 's': 18}

trantab2 = "abcdefghijklmnopqrs"

pattern_nodes = re.compile(r'[BW]\[\w{2}\]')
pattern_players = re.compile(r'P[BW]\[.+?\]')


def write(mode):
    '''导出sgf文件'''
    if mode.nodes:
        sgf_strs = map(sql2sgf, mode.nodes)
        with open(mode.title + '.sgf', 'w') as fp:
            fp.write('(' + ''.join(sgf_strs) + ')')
 

def sql2sgf(node):
    
    x, y, color = node
    if color == 1:
        player = 'B'
    elif color == -1:
        player = 'W'
    else:
        raise Exception("未定义的颜色")
    return ";{0}[{1}{2}]".format(player, trantab2[x], trantab2[y])


def sgf2sql(sgf_str):
    
    if sgf_str[0] == 'B':
        color = 1
    elif sgf_str[0] == 'W':
        color = -1
    else:
        raise Exception("未定义颜色")
    x = trantab[sgf_str[2]]
    y = trantab[sgf_str[3]]
    return(x, y, color)


def read(name):
    '''按文件导入棋谱'''
    if name.endswith('.sgf') or name.endswith('.SGF'):
        with open(name) as fp:
            qipu = fp.read()
        nodes = pattern_nodes.findall(qipu)
        players = pattern_players.findall(qipu)
        
        _nodes = map(sgf2sql, nodes)
        _name = ','.join(players)
        
        expert.insert(list(_nodes), _name)


def readdir(dirname):
    '''按目录导入棋谱'''
    processed_dirname = "已导入" + dirname
    if not os.path.exists(processed_dirname):
        os.mkdir(processed_dirname)
    
    files = os.listdir(dirname)
    for file in files:
        fullfile = os.path.join(dirname, file)
        if os.path.isfile(fullfile):
            read(fullfile)
            shutil.move(fullfile, processed_dirname)