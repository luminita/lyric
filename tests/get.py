import urllib2
response = urllib2.urlopen('http://ws.spotify.com/search/1/track.json?q=trubbel')
print response.info()
html = response.read()
print html
