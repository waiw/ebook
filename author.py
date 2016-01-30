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
import get_html

host = 'http://wx.ty2016.net'

def author(url):
	response = urllib.urlopen(url)
	result = response.read()
	soup = BeautifulSoup(result, "html.parser")
	#print soup.find_all('div')
	div = soup.find('div', attrs={'class':'content'})
	print div
	for line in div.find_all('a', href=True):
		url = host + line['href']
		print url
		get_html.get_book(url)
		# test with just one file
		#break

url = sys.argv[1]
author(url)
