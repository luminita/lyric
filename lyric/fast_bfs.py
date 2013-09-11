"""
This module gives a solution to the problem using a BFS algorithm 
"""
import sys
from solution import Solution
import webapi


class FastBFSSolution(Solution): 
    @staticmethod    
    def get_path(words, cache_dict):
        """
        Attempts to find a path between position 0 to position n-1 
        The input is a lists of lists, L, such that L[i] gives the list of 
        indices j>=i such that the words i i+1 ... j correspond to a song name 
        Each list L[i] should be sorted from smallest to largest index 
        """
        n = len(words)
        L = [[] for i in range(n)]
        M = [[] for i in range(n)]        
        # keep a stack where the possible paths are incrementally expanded
        stack = [(0, j) for j in range(0, n)]
        # record the path for backtracking 
        path = []
        found = False
        while len(stack)>0:
            (parent, end) = stack.pop()    
            sub_sentence = " ".join(words[parent:end+1]).strip()
            spotify_id = webapi.search_track(sub_sentence, cache_dict)
            while spotify_id == None:
                if len(stack) == 0:
                    return None
                (parent, end) = stack.pop()    
                sub_sentence = " ".join(words[parent:end+1]).strip()
                spotify_id = webapi.search_track(sub_sentence, cache_dict)
            M[parent].append(spotify_id)
            L[parent].append(end)            
            path.append((parent, end))
            # a path is found when position n-1 is reached
            if end == (n-1):
                found = True        
                # return at the first path 
                return path, L, M
            else:        
                # a solution is not reached, further expand the path             
                stack += [(end+1, i) for i in range(end+1, n)]    
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
        # get a solution if it exists
        ret = FastBFSSolution.get_path(words, cache_dict)
        if ret:
            path, L, M = ret
            # backtrack back 
            solution_path = FastBFSSolution.backtrack(path, len(L))
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
    pass


if __name__ == '__main__':
    main()
