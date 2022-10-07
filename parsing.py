#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:12:40 2019

@author: simransetia
"""
import datetime 
from spacy.lang.en import English
import xml.etree.cElementTree as ec
#tree = ec.parse('/Users/simransetia/Documents/simran/Others/QWiki code/week9wiki.xml')
tree = ec.parse('/Users/simransetia/Documents/Dataset/Area.xml')
root = tree.getroot()
rev_list=[]
time=[]
for page in root:
    for child in page:
        if 'revision' in child.tag:
            for each in child:
                if 'text' in each.tag:
                    s=str(each.text)
                    rev_list.append(s)
                if 'timestamp' in each.tag:
                    rev_date=str(each.text)
                    date2,time2=rev_date.split('T')
                    time2=time2.replace('Z','')
                    date_time_article=date2+' '+time2
                    date_time_obj= datetime.datetime.strptime(date_time_article, '%Y-%m-%d %H:%M:%S')
                    time.append(date_time_obj)

duration=time[len(time)-1]-time[0]
print(duration.days)
            
print(len(rev_list[len(rev_list)-1].split()))
                    
