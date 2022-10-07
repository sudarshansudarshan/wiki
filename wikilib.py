import requests
import io

def download_wiki_dataset(wiki_title):
    """Given the wikipedia article wiki_title
    download it to the current directory"""
    file_handler = io.open("./"+wiki_title+'.xml', mode='w+', encoding='utf-8')
    url = 'https://en.m.wikipedia.org/w/index.php?title=Special:Export&pages=' + wiki_title + '&&history=1&action=submit'
    #url='http://sccilabs.org/jocwiki2/index.php/Special:Export' + articleName + '&history=1&action=submit'
    #url='http://sccilabs.org/jocwiki2/index.php/?title=Special:Export&pages='+ articleName + '&curonly=0&action=submit'
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
