import random
import io
import os
import json
import mwclient
import re
import requests
import time
import xml.etree.cElementTree as ec
import wikitextparser as wtp


def download_wiki_dataset(wiki_title):
    """Given the wikipedia article wiki_title download it to the current directory"""
    """Copied from Simran's Repository"""
    file_handler = io.open("./"+wiki_title+'.xml', mode='w+', encoding='utf-8')
    url = 'https://en.m.wikipedia.org/w/index.php?title=Special:Export&pages=' + wiki_title + '&&history=1&action=submit'
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'}
    print('Downloading ' + wiki_title + '...') 
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        xml = r.text
        file_handler.write(xml)
        print(wiki_title,'Completed!')
    else:
        print('Something went wrong! ' + wiki_title + '\n' + '\n')
    file_handler.close()

def get_no_revisions(wiki_xml_file):
    """Given the wiki_xml_file returns number of revisions/edits"""
    tree=ec.parse(wiki_xml_file)
    root=tree.getroot()
    return (len(root[1])-3) #not sure if this is the right approach as we may potentially encounter other types of pages/tags @akhil - Jayanth


#May be this method can be imporved 
def get_latest_snapshot(wiki_xml_file):
    """Given the wiki_xml_file returns the latest snapshot of the wiki article"""
    tree= ec.parse(wiki_xml_file)
    root=tree.getroot()
    try:
        return root[1][-1][-2].text
    except IndexError:
        return ''

def get_no_unique_editors(wiki_xml_file):
    """Given the wiki_xml_file returns the number of unique editors/ips who edited the article"""
    tree= ec.parse(wiki_xml_file)
    root=tree.getroot()
    editor_ids=set()
    for sub_root in root:
        if 'page' in sub_root.tag:
            for sub_page in sub_root:
                if 'revision' in sub_page.tag:
                    for sub_revision in sub_page:
                        if 'contributor' in sub_revision.tag:
                            for sub_contributor in sub_revision:
                                if ('ip' in sub_contributor.tag) or ('id' in sub_contributor.tag):
                                    editor_id=sub_contributor.text
                                    editor_ids.add(editor_id)
    return len(editor_ids)

def get_no_references(snapshot):
    """Given a snapshot of the wiki page returns the number of references in the snapshot"""
    """Observations:
        1) Referencing something once they use '<ref>"something"</ref>"
        2) When they need to use a single reference multiple times they name it and reference it this way first time '<ref name="something">"something"</ref>' and this way from second time '<ref name="something" />'"""
    pattern='</ref>'
    count=0
    for _ in re.finditer(pattern, snapshot):
        count+=1
    return count

def get_wiki_article_json(article_name):
    """ This code is copied from stack overflow : https://stackoverflow.com/questions/45193005/download-entire-history-of-a-wikipedia-page
    This creates several json files in the current directory. Each json file
    corresponds to a revision history. I have checked this for a couple of
    cities and it is working fine. It is also very fast - Sudarshan"""

    base_path=os.getcwd()
    site = mwclient.Site('en.wikipedia.org')
    page = site.pages[article_name]
    try:
        os.mkdir(article_name)
    except FileExistsError:
        print('The directory already exisits please check')
        return
    os.chdir(article_name)
    for i, (info, content) in enumerate(zip(page.revisions(), page.revisions(prop='content'))):
        info['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", info['timestamp'])
        print(i, info['timestamp'])
        open("%s.json" % info['timestamp'].replace(':','_'), "w").write(json.dumps(
            { 'info': info,
                'content': content}, indent=4))
    os.chdir(base_path)

def get_table(snapshot):
    """
    This function returns a list of tables which are tables in the wikiarticle
    """
    parsed=wtp.parse(snapshot)
    tables=[table.data() for table in parsed.tables]
    return tables
    

def get_info_box(snapshot):
    """The function returns the infobox of a wikiarticle as a dictionary"""
    pattern="\{\{Infobox"
    k=re.search(pattern, snapshot)
    idx=k.span()[0]+2
    string=""
    stac=['{','{']
    while stac:
        char=snapshot[idx]
        string+=char
        if char in ['}',']',')']:
            stac.pop()
        if char in ['{','[','(']:
            stac.append(char)
        idx+=1
    string=string[:-2]
    return get_dict_from_string(string)

def get_dict_from_string(string):
    """Given a string of the form 'k\n|a=b\n|c=d\n|....' return a dictionary D={a:b,c:d....}"""
    line=""
    stack=[]
    stack_string=''
    box=dict()
    for char in string:
        if char in '{[':
            stack.append(char)
        if char in '}]':
            stack.pop()
            if stack==[]:
                stack_string+=char
        if char =='|' and stack==[]:
            if '=' not in line:
                line=''
                continue
            if not stack_string:
                a,b=line.split('=')
                a=re.sub('(^\s*| \s+|\s*$| ?\n)','',a)
                b=re.sub('(^\s*|\s*$| \s+| ?\n)','',b)
                box[a]=b
            if stack_string:
                idx=line.find('=')
                a=line[:idx]
                a=re.sub('(^\s*| \s+|\s*$| ?\n)','',a)
                b=line[idx+2:]
                b=re.sub('(^\s*|\s*$| \s+| ?\n)','',b)
                box[a]=b
            line=''
            stack_string=''
            continue
        line+=char
        if stack:
            stack_string+=char
    return box

def get_out_going_links(snapshot):
    """The function returns the list of wiki articles mentioned in the wikiarticle"""
    parsed=wtp.parse(snapshot)
    out_links=[]
    for link in parsed.wikilinks:
        out_links.append(link.target)
    return out_links

def Create_Dummy_Bigfile(k):
    """This will create a file with k lines"""
    f=open('dummy.txt','a+')
    for i in range(k):
        f.write(str(random.random()))
        f.write('\n')
    f.close()

