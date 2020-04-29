#!/usr/bin/python

from urllib.request import urlopen
# import urllib2
url = "https://fd-distribution.pl/xml-porownywarki/sellyshop/index-eur.php?hash=zdefiniuj-haslo"
s = urlopen(url)
contents = s.read()
file = open("export.xml", 'w', encoding="utf8")
file.write(str(contents.decode('utf-8')))
file.close()