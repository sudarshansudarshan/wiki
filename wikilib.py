from logging import root
import requests
import io
import xml.etree.cElementTree as ec


def download_wiki_dataset(wiki_title):
    """Given the wikipedia article wiki_title
    download it to the current directory"""
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
    tree= ec.parse(wiki_xml_file)
    root=tree.getroot()
    snapshot=''
    for sub_root in root:
        if 'page' in sub_root.tag:
            for sub_page in sub_root:
                if 'revision' in sub_page.tag:
                    for sub_revision in sub_page:
                        if 'text' in sub_revision.tag:
                            snapshot=sub_revision.text
    return snapshot

def get_no_unique_editors(wiki_xml_file):
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