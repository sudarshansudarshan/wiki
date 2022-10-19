"""
This python program will consider a city and extract all the proper nouns from
the city and create a list of words with their time of arrival, in the revision
history. 

*India is a country in south asia. The place is more of a sub-continent than a
country. There are 26 languages spoken in the country with *Hindi being one of
the widely used official language. India got its independence on 15th of August
1947. Although, many freedom fighters were involved in the freedom struggle,
*Mahatma *Gandhi is considered to have played a major role. Post Independence,
the country got sub-divided into states with *Delhi being the capital.
*Bangladesh and *Pakistan saw itself distancing from the country, thus creating
the partition of this region for the first time in the documented history 

(There are a total of 7 proper nouns in the above paragraph.) 
"""
from math import log, exp
import numpy as np
import spacy
import json
import datetime
nlp = spacy.load("en_core_web_sm")

def list_of_articles(article_list):
    """


    """

def extract_timeseries_propernouns(article_name):
    """
    Given an article_name, let us say _India_, we need to extract all the
    proper nouns across the revision history of the given article and return a
    list in the form: [(time,timestep,no_propernouns),...]. Where time is the
    date/time of revision, timestep represents the
    revision history number and the no_propernouns is the total number of
    proper nouns added in that revision history.
    List of tasks:
    1) Download the master json file: Jayant
    2) Read the json file, one revision at a time and populate the triple as
    stated above: Nivedita/Shahid.
    """
    filename=article_name+".json"
    f= open(filename)
    data= json.load(f)
    fmt = '%Y-%m-%dT%H:%M:%S'
    timestep=0
    L=[]
    k= data.keys()
    for key in k:
      #timestep= data[key]["info"]["revid"]
      timestep+=1
      time= data[key]["info"]["timestamp"]
      tstamp = str(datetime.datetime.strptime(time, fmt))
      #print(tstamp)
      text=data[key]["content"]["*"]
      current_propernouns= propernouns(text)
      t= (tstamp, timestep, len(current_propernouns))
      L.append(t)

    #print(L)
    return L

def get_upper_limit(data):
    """
    Let ae^(bx) is graph of data, log of this will be log(a) +bx.
    here a is obviously positive.
    """
    x = []
    y = []

    for i in data:
        x.append(i[0])
        y.append(log(i[1]))

    z = np.polyfit(x, y, 1)

    return exp(z[1])

def propernouns(s):
    """
    Given a string s, return the proper nouns as a set
    """
    doc = nlp(s)
    pronouns = set()
    for tok in doc:
        if tok.pos_ == "PROPN":
            pronouns.add(tok.text)
    return pronouns

def master_json(article_name):
    """
    Given the article_name create a master json file containing all the
    revisions. Include more details on this docstring.
    """

    from wikilib import get_wiki_article_json
    import os
    import shutil
    base_path=os.getcwd()
    get_wiki_article_json(article_name)
    master_json= open("%s.json"%article_name,'w')
    master_json.write('{\n')
    os.chdir(article_name)
    json_list=os.listdir()  #not sure if this will return file_list in ascending order
    for idx in range(len(json_list)):
        json_file=json_list[idx]
        f=open(json_file,'r')
        json_file=json_file.replace('.json','')
        master_json.write('"%s":'%json_file)
        master_json.write(f.read())
        f.close()
        if idx==len(json_list)-1:
            continue
        master_json.write(',')
    master_json.write('}')
    os.chdir(base_path)
    shutil.rmtree(article_name)
    master_json.close()