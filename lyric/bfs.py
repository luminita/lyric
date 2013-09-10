"""
This module gives a solution to the problem using a BFS algorithm 
"""
import sys
from solution import Solution
import webapi


class BFSSolution(Solution): 
    
    @staticmethod    
    def build_matrix(words, cache_dict):
        """ Given a list of words, build a matrix L such that L[i] includes 
        all the indices j>=i such that the sub-sentence from words i to 
        j corresponds to a song. The elements of each L are sorted in ascending
        order 
    
        Another matrix M similar to L is built where M[i][j] gives the
        spotify id for L[i][j]     
            
        As an example, if the message is "If I can't let it go", and the only songs 
        found starting from the word "If" were 
        "If I can't", spotify id 6mcu7D7QuABVwUGDwovOEh and 
        "If I can't let", spotify id 89fegffSHJwUG768HJHvsd then 
        L[0] = [2, 3] 
        M[0] = ["6mcu7D7QuABVwUGDwovOEh", "89fegffSHJwUG768HJHvsd"] """        
        L = [[] for i in range(len(words))]
        M = [[] for i in range(len(words))]
        for i in range(len(words)):        
            sub_sentence = ""
            for j in range(i, len(words)):                
                sub_sentence += " " + words[j] 
                sub_sentence = sub_sentence.strip()
                spotify_id = webapi.search_track(sub_sentence, cache_dict)
                if spotify_id != None:
                    L[i].append(j)
                    M[i].append(spotify_id)     
        return L, M
    
    
    @staticmethod    
    def get_path(L):
        """
        Attempts to find a path between position 0 to position n-1 
        The input is a lists of lists, L, such that L[i] gives the list of 
        indices j>=i such that the words i i+1 ... j correspond to a song name 
        Each list L[i] should be sorted from smallest to largest index 
        """
        n = len(L)
        # keep a stack where the solution is incrementally built;
        stack = [(0, L[0][i]) for i in range(0, len(L[0]))]
        # record the path for backtracking 
        path = []
        found = False
        while len(stack)>0:
            (parent, end) = stack.pop()    
            path.append((parent, end))
            # a path is found when position n-1 is reached
            if end == (n-1):
                found = True        
                # return at the first path 
                return path
            else:        
                # a path is not reached, further expand the list
                stack += [(end+1, L[end+1][i]) for i in range(0, len(L[end+1]))]    
        if not found:
            return None
            
            
    @staticmethod 
    def backtrack(path, n):
        """ Backtrack on the path and return a list of indices in the sequence """
        i = len(path)-1
        # backtrack from position n-1 
        to_find = n-1
        path_solution = []        
        while i>=0:        
            (parent, child) = path[i]    
            while child != to_find and i>0:
                i = i-1
                (parent, child) = path[i]    
            path_solution = [(parent, child)] + path_solution
            # we reached the beginning of the path
            if parent == 0:
                break
            to_find = parent-1                
            i = i-1            
        return path_solution


    @staticmethod    
    def get_solution(words, cache_dict, playlist_base):
        """ Giving a list of words, this class should return a list of pairs 
        (song name, spotify online link) """       
        # build the matrices where we search all subsentences 
        L, M = BFSSolution.build_matrix(words, cache_dict)
        # get a path through this matrix
        path = BFSSolution.get_path(L)
        if path:
            # backtrack back 
            solution_path = BFSSolution.backtrack(path, len(L))
            # build the playlist from the track 
            playlist = []
            for (start, end) in solution_path:
                k = 0
                while k < len(L[start]) and L[start][k] != end:
                    k += 1            
                track = " ".join(words[start:end+1])
                online_address = playlist_base + M[start][k] 
                playlist.append((track, online_address))
            return playlist
        return None
    

def main():
    L = [[0,1], [1,2,3], [2], [3], [4,6], [5,7], [], [7,8], []]
    L = [[0], [1,2,3], [2], [3], [4,6], [5,7], [], [7,8], []]
    path = get_path(L)
    solution_path = backtrack(path, len(L))
    print solution_path


if __name__ == '__main__':
    main()

"""        
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

"""
