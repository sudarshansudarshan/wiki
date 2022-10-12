import requests
import io
import xml.etree.cElementTree as ec
import re


def download_wiki_dataset(wiki_title):
    """Given the wikipedia article wiki_title download it to the current directory"""
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
    rev_count=0
    for sub_root in root:
        if 'page' in sub_root.tag:
            for sub_page in sub_root:
                if 'revision' in sub_page.tag:
                    rev_count+=1
    return rev_count


#May be this method can be imporved 
def get_latest_snapshot(wiki_xml_file):
    """Given the wiki_xml_file returns the latest snapshot of the wiki article"""
    tree= ec.parse(wiki_xml_file)
    root=tree.getroot()
    snapshot=''
    try:
        return root[1][-1][-2].text
    except:
        return ''
    
    for sub_root in root:
        if 'page' in sub_root.tag:
            for sub_page in sub_root:
                if 'revision' in sub_page.tag:
                    for sub_revision in sub_page:
                        if 'text' in sub_revision.tag:
                            snapshot=sub_revision.text
    return snapshot

def get_no_unique_editors(wiki_xml_file):
    """Given the wiki_xml_file returns the number of unique editors/ips who edited the article"""
    tree= ec.parse(wiki_xml_file)
    root=tree.getroot()
    editor_ids=[]
    for sub_root in root:
        if 'page' in sub_root.tag:
            for sub_page in sub_root:
                if 'revision' in sub_page.tag:
                    for sub_revision in sub_page:
                        if 'contributor' in sub_revision.tag:
                            for sub_contributor in sub_revision:
                                if ('ip' in sub_contributor.tag) or ('id' in sub_contributor.tag):
                                    editor_id=sub_contributor.text
                                    if editor_id not in editor_ids:
                                        editor_ids.append(editor_id)
    return len(editor_ids)

def get_no_references(snapshot):
    """Given a snapshot of the wiki page returns the number of references in the snapshot"""
    """Observations:
        1) Referencing something once they use '<ref>"something"</ref>"
        2) When they need to use a single reference multiple times they name it and reference it this way first time '<ref name="something">"something"</ref>' and this way from second time '<ref name="something" />'"""
    pattern='<\/ref>'
    count=0
    for _ in re.finditer(pattern, snapshot):
        count+=1
    return count

def get_wiki_article_json(article_name):
    """ This code is copied from stack overflow : https://stackoverflow.com/questions/45193005/download-entire-history-of-a-wikipedia-page
    This creates several json files in the current directory. Each json file
    corresponds to a revision history. I have checked this for a couple of
    cities and it is working fine. It is also very fast - Sudarshan"""
    import mwclient
    import json
    import time

    site = mwclient.Site('en.wikipedia.org')
    page = site.pages[article_name]

    for i, (info, content) in enumerate(zip(page.revisions(), page.revisions(prop='content'))):
        info['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", info['timestamp'])
        print(i, info['timestamp'])
        open("%s.json" % info['timestamp'], "w").write(json.dumps(
            { 'info': info,
                'content': content}, indent=4))
