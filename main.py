from typing import Union
import json
from flask import jsonify
from flask import Flask
from flask import render_template
app = Flask(__name__)
import pandas as pd
from flask_cors import CORS,cross_origin
CORS(app)



import itertools
import random
import numpy as np
word_list=[]
file_path='./WORDS.txt'
# List of 5-letter words
with open(file_path, 'r') as f:
    word_list = [line.strip() for line in f]
wordlistdic={}
# Create function to validate crossword formation
'''
for word in word_list:
    flist={1:[],3:[],5:[]}
    counter_1=0
    counter_2=0
    counter_3=0
    counter_4=0
    counter_5=0
    for nword in word_list:
        if nword != word:
            if (nword[0]==word[0]):
                flist[1].append(nword)
                counter_1=1
            if (nword[0]==word[2]):
                flist[3].append(nword)
                counter_2=1
            if (nword[0]==word[4]):
                flist[5].append(nword)
                counter_3=1
            if (counter_1==1 and counter_2==1 and counter_3==1):
                wordlistdic[word]=flist
print(wordlistdic['pamir'])
print(len(wordlistdic))
'''

tripdict={}
for word in word_list:
    tkey=word[0]+word[2]+word[4]
    if tkey not in tripdict.keys():
        tripdict[tkey]=[word]
    else:
        tripdict[tkey].append(word)
    
karray=list(tripdict.keys())
#karray=['cgr','cap','gie','rmn','aim','pen','asd','tup','rem','nah']
def checkwords(kword1,kword2,kword3):
    kword4=kword1[0]+kword2[0]+kword3[0]
    kword5=kword1[1]+kword2[1]+kword3[1]
    kword6=kword1[2]+kword2[2]+kword3[2]
    #print([kword4,kword5,kword6])
    if ((kword4 in karray) and (kword5 in karray) and (kword6 in karray)):
        return [kword4,kword5,kword6]
    else:
        return False
valid_combo=[]

#def getcombo():
Ntot=len(karray)
num=np.floor(np.random.random(1)*Ntot)
num=num.astype(np.int64)
combo_counter=0
combo_list=[]
k=num[0]
if k==num[0]:
    for i in range(len(karray)):
        for j in range(len(karray)):
            if i!=j and j!=k and i!=k:
                kword1=karray[k]
                kword2=karray[i]
                kword3=karray[j]
                kwordall=[kword1,kword2,kword3]
                #print(['inpword',kword1,kword2,kword3])
                combo=checkwords(kword1,kword2,kword3)
                if (combo!=False) and (combo[0] not in kwordall) and (combo[1] not in kwordall) and (combo[2] not in kwordall) :
                    #print('got the combo!')
                    combo_list.append([kword1,kword2,kword3]+combo)
                    combo_counter+=1
        if combo_counter>50:
            print('reached 50')
            break
                #else:
                #   getcombo()

ctot=len(combo_list)
cnum=np.floor(np.random.random(1)*ctot)
cnum=cnum.astype(np.int64)
print(combo_list[cnum[0]])
tword_list=combo_list[cnum[0]]
def getWordFromCombo(tword):
    finum=len(tripdict[tword])
    anum=np.floor(np.random.random(1)*finum)
    anum=anum.astype(np.int64)
    print(anum)
    return tripdict[tword][anum[0]]
final_words=[]
unqsol=1
print(tword_list)
for word in tword_list:
    while(unqsol!=0):
        fword=getWordFromCombo(word)
        print(fword)
        if fword  not in final_words:
            final_words.append(fword)
            print(final_words)
            unqsol=0
    unqsol+=1
    print(unqsol)

print(final_words)
state_grid=np.empty((5,5),dtype=str)
letcheck1=np.empty((5,5),dtype='U25')
letcheck2=np.empty((5,5),dtype='U25')



wordc=0
for word in final_words:
    print(word)
    nword=list(word)
    if wordc==0:
        state_grid[0,:]=nword
    if wordc==1:
        state_grid[2,:]=nword
    if wordc==2:
        state_grid[4,:]=nword
    if wordc==3:
        state_grid[1,0]=nword[1]
        state_grid[3,0]=nword[3]
    if wordc==4:
        state_grid[1,2]=nword[1]
        state_grid[3,2]=nword[3]
    if wordc==5:
        state_grid[1,4]=nword[1]
        state_grid[3,4]=nword[3]
    wordc+=1

print(state_grid)
print(final_words[0])
for i in range(5):
    letcheck1[0,i]=final_words[0]
    letcheck1[2,i]=final_words[1]
    letcheck1[4,i]=final_words[2]
    letcheck2[i,0]=final_words[3]
    letcheck2[i,2]=final_words[4]
    letcheck2[i,4]=final_words[5]



letcheck=letcheck1+letcheck2
print(letcheck)
#val=getcombo()

#print(val)
#print(checkwords('cgr','aim','pen'))


import random

# Initial 5x5 grid with empty spots at (1,1), (3,3), (1,3), and (3,1)
newgrid = np.copy(state_grid)

# Step 1: Extract all non-empty letters
letters = [newgrid[i,j] for i in range(5) for j in range(5) if (i, j) not in [(1, 1), (3, 3), (1, 3), (3, 1),(0,0)]]



# Step 2: Shuffle the list of letters
random.shuffle(letters)
random.shuffle(letters)
random.shuffle(letters)
random.shuffle(letters)

print(state_grid)
# Step 3: Place the shuffled letters back, ensuring empty spots stay empty
index = 0
for i in range(5):
    for j in range(5):
        if (i, j) not in [(1, 1), (3, 3), (1, 3), (3, 1),(0,0)]:
            newgrid[i,j] = letters[index]
            index += 1

# Print the shuffled grid
print(newgrid)





print(state_grid)
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/correct/<letter>/<int:first>/<int:second>")
@cross_origin()
def read_item(letter,first,second):
    if(state_grid[first-1][second-1]==letter):
        response = jsonify({"letter":1})
    elif(letter in letcheck[first-1][second-1]):
        response = jsonify({"letter":2})
    else:
        response = jsonify({"letter":0})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/letters/<int:first>/<int:second>")
@cross_origin()
def read_item1(first,second):
    response = jsonify({"letter":newgrid[first-1][second-1]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



