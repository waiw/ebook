#! /usr/bin/env python
# ssh -p 29418 review-android.quicinc.com gerrit query --current-patch-set --format TEXT project:graphics/adreno200 branch:master limit:10 is:open label:Code-Review+2 label:DeveloperVerified+1

import os
import subprocess
import simplejson
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






def save_to_txt(link, log):
	response = urllib.urlopen(link)
	result = response.read()
	soup = BeautifulSoup(result, "html.parser")
	print soup.title.string
	log.write(soup.title.string.encode('utf-8'))
	log.write('\n\n')
	# These two are the same
	#print soup.find_all('p')
	for line in soup.find_all('p'):
		line = replace_with_newlines(line)
		#print line
		log.write(line.encode('utf-8'))
		#print soup.p.encode('utf-8')
		#print soup.p.encode('gb2312')
		#print soup.p.encode('gbk')
		#print soup.p.stripped_strings


url = 'http://wx.ty2016.net/book/gl01/'
#url = 'http://wx.ty2016.net/book/gl01/424.html'
url2 = 'http://wx.ty2016.net/book/gl01/425.html'

response = urllib.urlopen(url)
result = response.read()
soup = BeautifulSoup(result, "html.parser")
print soup.title.string
log = open(soup.title.string+".txt", "w")
for line in soup.dl.find_all('a', href=True):
	url2 = url + line['href']
	print url2
	save_to_txt(url2, log)
log.close()
