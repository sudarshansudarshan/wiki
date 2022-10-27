import bz2, time, nltk
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
    n=200*(1000**2)
    counter=0
    S=set([])
    with bz2.open('../enwiki-latest-pages-articles.xml.bz2','rb') as f:
        while True:
            g=open('all_words.txt','a')
            counter=counter+1
            print((counter),"%")
            s=f.read(n)
            L=s.split(b' ')
            #print(L)
            if not L:
                break
            for i in range(len(L)):
                x=str(L[i])
                y=x[2:-1]
                if y in Words and y not in S:
                    print(i,len(L),y)
                    S.add(y)
                    g.write(y+'\n')
            g.close() 

exp()

