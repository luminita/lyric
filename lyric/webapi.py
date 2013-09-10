# -*- coding: utf-8 -*- 
"""
Provides the ability to interact with the Spotify web API
by using simple HTTP GET messages
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
    """ Get the name and spotify href id for the track in 
    data that matches exactly the track. Return None if no track
    matches precisely """
    tracks = data["tracks"]
    i = 0 
    while i < len(tracks):
        name = tracks[i]["name"].lower()
        name = name.encode('utf-8')
        print name, " -- ", track, "---", tracks[i]["href"].split(":")[2] 
        if name.strip() == track.strip():
            spotify_id = tracks[i]["href"].split(":")[2]
            return spotify_id
        i += 1
    return None        
 

def search_track(track, base="http://ws.spotify.com/search/1/"):
    """ searches the track_name and returns the unique code 
    of the track if an exact match is found, and None otherwise. """
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
    except Exception, e:
        sys.exit(str(e))

    # load result in json format 
    data = json.load(response)
    # get the code of the first exact match in the data 
    spotify_id = get_matching_track(low_case_track, data)
    
    return spotify_id   


def main():
    x = "Aldrig ska jag sluta Älska Dig"
    print search_track(x)

if __name__ == "__main__":
    main()
