import bz2, time, nltk,os
import pdb
pdb.set_trace()



def niv_exp():
    t0 = time.time()
    i = 0
    s = b''

    with bz2.open('../enwiki-latest-pages-articles.xml.bz2','rb') as f:
        while True:
            s += f.read(10*6)
            L = s.split(b'\n') 
            print(L)
            if not L:
                break
            for l in L[:-1]:   
                i += 1
                if i % 100000 == 0:
                    print('%i lines/sec' % (i/(time.time() - t0)))
            s = L[-1]          

def exp():
    """Takes all words in the file and displays it. The buffer size is n"""
    Words=list(nltk.corpus.words.words())
    Words=set(Words)
    n=(1000**2)*10
    counter=0
    S=set([])
    with open('/Users/sudarshaniyengar/Desktop/all_articles/enwiki-latest-pages-articles.xml','r') as f:
        while True:
            g=open('all_words.txt','a')
            counter=counter+1
            #print((n*counter),"Mb")
            os.system('sleep 1')
            s=f.read(n)
            L=s.split(' ')
            #print(L)
            if (not L) or (len(L)==1 and L[0]==''):
                break
            for i in range(len(L)):
                x=str(L[i])
                y=x
                if y in Words and y not in S:
                    #print(i,len(L),y)
                    S.add(y)
                    g.write(y+'\n')
            g.close() 
            
            
def get_city_articleid():
  import requests
  import csv

  page_titles = ['Mumbai', 'Indore']

  for each in page_titles:
    url = (
        'https://en.wikipedia.org/w/api.php'
        '?action=query'
        '&prop=info'
        '&inprop=subjectid'
        '&titles=' + '|'.join(each) +
        '&format=json')
    json_response = requests.get(url).json()

    title_to_page_id  = {
        page_info['title']: page_id
        for page_id, page_info in json_response['query']['pages'].items()}

    x=title_to_page_id
    print(title_to_page_id)
    with open('cities_articles_id.csv', 'w+') as f:
        for key in x.keys():
            f.write("%s, %s\n" % (key, x[key]))
        f.close()

t1=time.time()

exp()

t2=time.time()
print(t2-t1,"seconds")
