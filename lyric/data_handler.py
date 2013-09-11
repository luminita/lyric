# -*- coding: utf-8 -*- 
"""
Provides functions to read, write and process data
"""
import re


def parse_message(message, punctuation_marks="!|\.|;|\?|:"):
    """ Splits the message in sentences at each occurence of any of the 
    punctuation marks. Return a list of sentences """
    # split the message in sentences
    sentences = re.split(punctuation_marks, message)
    # remove empty sentences and any spaces in the beginning or end of the sentence
    # All \n are replaced with with space
    sentences = [l.strip().replace("\n", " ") for l in sentences \
                if len(l.strip()) > 0]   
    return sentences 
            
    
def load_message(filename):
    """ Load the message from a file. Return a list of sentences """
    try:
        lines = open(filename).readlines()
        message = "".join(lines)
    except Exception, e:
        sys.exit(str(e))
    return parse_message(message)
    
    
def print2file(lines, filename):
    """ Print a list of lines to a file. Note that each line should include
    the newline character """
    try:    
        outf = open(filename, "w")
        for l in lines:
            outf.write(l)
        outf.close()
    except Exception, e:
        sys.exit(str(e))
    
    
    
def main():
    mesg = "Allt! bra. All : vad ; ar \n best"
    print parse_message(mesg.decode('utf-8'))
    print load_message("../examples/example_2.txt")


if __name__ == '__main__':
    main()
