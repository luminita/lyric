# -*- coding: utf-8 -*- 
"""
Provides functions to interact with the Spotify web API by using simple 
HTTP GET messages
"""
import urllib2
import urlparse
import json
import sys


class MyError(Exception): 
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def get_url(track, base):
    """ get the exact URL for the HTTP request. Assume the track
    is lower case """
    # replace spaces with plus
    track2search = track.replace(" ", "+")
    format_track = "track.json?q="+track2search 
    url = urlparse.urljoin(base, format_track)     
    return url 


def get_matching_track(track, data):
    """ Get the spotify href id for the track in the data that 
    matches exactly the track. Return None if no track is exact match """
    tracks = data["tracks"]
    i = 0 
    while i < len(tracks):
        name = tracks[i]["name"].lower()
        name = name.encode('utf-8')        
        if name.strip() == track.strip():            
            spotify_id = tracks[i]["href"].split(":")[2]
            return spotify_id
        i += 1        
    return None        
 

def search_track(track, cache_dict, base="http://ws.spotify.com/search/1/"):
    """ searches the track_name and returns the unique code 
    of the track if an exact match is found, and None otherwise. """
    if track in cache_dict:
        return cache_dict[track]
    low_case_track = track.decode('utf-8').lower()
    low_case_track = low_case_track.encode('utf-8')    
    url = get_url(low_case_track, base)        
    try: 
        # send the request the easy way
        response = urllib2.urlopen(url)
        # check that the request was successfully processed
        status_code = response.getcode()
        if status_code != 200:
           raise MyError("Error at HTTP request. Error status: {}".\
                         format(status_code))
        # load result in json format 
        data = json.load(response)
        # get the code of the first exact match in the data 
        spotify_id = get_matching_track(low_case_track, data)    
        cache_dict[track] = spotify_id
        return spotify_id   
    except Exception, e:
        sys.exit(str(e))

    


def main():
    x = "aldrig ska jag sluta älska dig"    
    print search_track(x, {})


if __name__ == "__main__":
    main()
