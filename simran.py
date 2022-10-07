#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 13:19:29 2019

@author: simransetia
"""

import requests
import io
from os import listdir
from os.path import isfile, join
# importing the module
import csv
from string import Template
# open the file in read mode
#filename = open('/Users/simransetia/Downloads/aap-combined-1.csv', 'r')

# creating dictreader object
#mypath='/Users/simransetia/Documents/Dataset/Pages/'
#mypath1='/Users/simransetia/Documents/Dataset/Talk_pages/'
#plist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#plist1=[f for f in listdir(mypath1) if isfile(join(mypath1, f))]

def get_wiki_byname(featuredArticleList):
	# articleName = raw_input()
	# articleName = articleName.replace(' ', '_')

	for each in featuredArticleList:
		articleName = each

		file_handler = io.open("./"+articleName+'.xml', mode='w+', encoding='utf-8')

		url = 'https://en.m.wikipedia.org/w/index.php?title=Special:Export&pages=' + articleName + '&&history=1&action=submit'
        #url='http://sccilabs.org/jocwiki2/index.php/Special:Export' + articleName + '&history=1&action=submit'
        #url='http://sccilabs.org/jocwiki2/index.php/?title=Special:Export&pages='+ articleName + '&curonly=0&action=submit'
		headers = {
			'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
		}
		print('Downloading ' + articleName + '...') 
		r = requests.get(url, headers=headers)
		if r.status_code == 200:
			xml = r.text
			file_handler.write(xml)
			print(articleName,'Completed!')
		else:
			print('Something went wrong! ' + articleName + '\n' + '\n')

		file_handler.close()

get_wiki_byname(['India'])
