import bz2, time
import pdb
pdb.set_trace()
t0 = time.time()
i = 0
s = b''
with bz2.open("/home/sscilabs/Data/latest-article/enwiki-latest-pages-articles.xml.bz2", 'rb') as f:
    while True:
        s += f.read(10*6)
        L = s.split(b'\n') 
        if not L:
            break
        for l in L[:-1]:   
            i += 1
            if i % 100000 == 0:
                print('%i lines/sec' % (i/(time.time() - t0)))
        s = L[-1]          
