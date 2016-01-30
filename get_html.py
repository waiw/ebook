#! /usr/bin/env python
# python get_html.py http://wx.ty2016.net/book/shendiaoxialv/

import os
import subprocess
import json as simplejson
import time
import sys
import types
import datetime
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

###########
# strip out <br> with new line

def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text






def save_to_html(link, line, new_soup):
        str = '<table width="800" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#ffffff"><a name='+line['href'].strip('.html')+'></a><tr><td width="800" height="45" align="center" bgcolor="#ffffff"><strong><font color="#000000" size="4">'+line.string+'</font><strong></td></tr></table>'
	soup = BeautifulSoup(str)
        new_soup.append(soup.table)
	response = urllib.urlopen(link)
	result = response.read()
	soup = BeautifulSoup(result, "html.parser")
	for table in soup.find_all('table'):
		p = table.find('p')
		#print p
		if p != None:
			new_soup.append(table)

url = sys.argv[1]

response = urllib.urlopen(url)
result = response.read()
soup = BeautifulSoup(result, "html.parser")
new_soup = BeautifulSoup("<head></head><body><h2></h2><h3></h3><p></p><dl></dl></body>")
print soup.title.string.encode('utf-8')
log = open(soup.title.string+".html", "w")
for line in soup.dl.find_all('a', href=True):
	url2 = url + line['href']
	save_to_html(url2, line, new_soup.body)
	line['href'] = '#'+line['href'].strip('.html')
	# test with just one file
	#break
new_soup.head.replace_with(soup.head)
new_soup.h2.replace_with(soup.body.h2)
new_soup.h3.replace_with(soup.body.h3)
new_soup.p.replace_with(soup.body.p)
new_soup.dl.replace_with(soup.body.dl)
log.write(str(new_soup))
log.close()
