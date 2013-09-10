import sys

sentence = "My PG's pusses are like juice in the morning".split(" ")
w = [[2], [2], [2], [5], [], [5], [8], [], []]
n = len(w)

def backtrack(path, sentence):
    i = len(path)-1
    to_find = n-1
    path_solution = []        
    words_solution = []        
    while i>=0:        
        (parent, child) = path[i]    
        while child != to_find and i>0:
            i = i-1
            (parent, child) = path[i]    
        path_solution = [(parent, child)] + path_solution
        words_solution = [sentence[parent:child+1]] + words_solution
        if parent == 0:
            break
        to_find = parent-1                
        i = i-1
            
    print path_solution
    print words_solution
        
        
def get_paths(w):
    stack = [(0, w[0][i]) for i in range(0, len(w[0]))]
    path = []
    while len(stack)>0:
        (parent, end) = stack.pop()    
        path.append((parent, end))
        if end == (n-1):        
            yield path
        else:        
            stack += [(end+1, w[end+1][i]) for i in range(0, len(w[end+1]))]


def get_path(w):
    stack = [(0, w[0][i]) for i in range(0, len(w[0]))]
    path = []
    found = False
    while len(stack)>0:
        (parent, end) = stack.pop()    
        path.append((parent, end))
        if end == (n-1):
            found = True        
            return path
        else:        
            stack += [(end+1, w[end+1][i]) for i in range(0, len(w[end+1]))]
    if not found:
        print "No solution!"
        sys.exit(1)

backtrack(get_path(w), sentence)
"""
for path in get_paths(w):
    print path
    backtrack(path, sentence)
    print "----------------------"
"""
