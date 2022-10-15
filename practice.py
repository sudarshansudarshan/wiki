import nltk
import bz2

print("Opening the bz2 file in the read mode")
f=bz2.open('enwiki-latest-pages-articles.xml.bz2','r')
D=[]
print("dictionary initialized")
print("Updating Dictionary....")
L=nltk.corpus.words.words()
print("Created a list of valid English words and updated the dictionary")

s='sudarshan'
count=0
first=00
second=0
Z=[]
for i in range(5000):
    count=count+1
    s=str(f.readline())
    W=s.split(sep=' ')
    #print(W)
    for word in W:
        if word in L:
            D.append(word)
    if count%10==0:
        print(count*10,"lines",len(D),"words","-->",second-first)
        first=second
        second=len(D)
    Z.append(len(D))

import matplotlib.pyplot as plt
plt.plot(Z)
plt.show()


