"""
Main body of the software
"""
import os 
import sys
from time import time
import argparse 
import data_handler
import bfs

# basename in front of the spotify id when outputing the playlist
PLAYLIST_BASE = "http://open.spotify.com/track/"

def get_method(method_string):
    if method_string == "bfs":
        return bfs.BFSSolution.get_solution   
    else:
        sys.exit("Unknown method {}".format(method_string))
 
 
def main():
    t0 = time()
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="Message or file name including the message",\
                       metavar="message", required=True)
    parser.add_argument('-m', help="Method to solve the problem [bfs], default = bfs", \
                        metavar="solving_method", required=False, default="bfs")     
    parser.add_argument('-o', help="Output file. By default the result is printed on the screen", \
                        metavar="out_file", required=False, default=None)        
    args = parser.parse_args()    
    mesg = args.i
    solving_method = get_method(args.m)
    out_file = args.o
    
    # process the input data 
    if os.path.isfile(mesg):
        sentences = data_handler.load_message(mesg)
    else:
        sentences = data_handler.parse_message(mesg)
    
    # find a solution for each sentence     
    cache_dict = {}
    result = []    
    for sentence in sentences:
        words = sentence.split()
        playlist = solving_method(words, cache_dict, PLAYLIST_BASE)                
        result.append("---------------\nSentence: {}\n--------------\n".\
                     format(sentence))
        if playlist == None:
            result.append("No perfect match found.\n")
        else:
            result += ["{} --> {}\n".format(p[0], p[1]) for p in playlist]
    
    # write the result to the output file or to the screen 
    if out_file != None:
        data_handler.print2file(result, out_file)
    else:
        for r in result:
            print str(r),     
            
    # execution time             
    t1 = time()
    print "\n############################################"  
    print "Analysis time: %.1f minutes" % ((t1 - t0) / 60)
    print "############################################"    
    
    
if __name__ == '__main__':
    main()
    
    
    
