from typing import Union
import json
from flask import jsonify
from flask import Flask
from flask import render_template
app = Flask(__name__)
from flask_cors import CORS,cross_origin
CORS(app)



import itertools
import random
import numpy as np
word_list=[]
##list of thousand most used words
file_path='api/WORDS.txt'
with open(file_path, 'r') as f:
    word_list = [line.strip() for line in f]
wordlistdic={}
# create a dictionary of words with keys based on 1st 3rd and 5th letter

tripdict={}
for word in word_list:
    tkey=word[0]+word[2]+word[4]
    if tkey not in tripdict.keys():
        tripdict[tkey]=[word]
    else:
        tripdict[tkey].append(word)
    
#list of keys
karray=list(tripdict.keys())


#function to find  valid 3 key combos for for given first three
#
#  a---b---c
#  |   |   |
#  d---e---f
#  |   |   |
#  g---h---i
# 
# For a given abc, def and ghi find adg, beh, and cfi
#
# #

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

#   1. Select randomly 1st 3-letter-key
#   2. Traverse the list of keys for 2nd and 3rd 3-letter-key
#   3. Check if combo works for the function,
#   4. select randomly 6 key combo.
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

#Get the word from 6 3-letter-combos make sure no words are repeated
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
#final selected 6 words

print(final_words)
state_grid=np.empty((5,5),dtype=str)
letcheck1=np.empty((5,5),dtype='U25')
letcheck2=np.empty((5,5),dtype='U25')



wordc=0
#put the words in grid of 5x5 with letters. M

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


#create letcheck matrix such that it has letters 
#  if the 6 words are 1,2,3,4,5,6
# then grid should be like suppose
# first letter is CRANE and 4th is CRUDE
# 0,0 will be cranecrude
# if letter C is solved the it should become ranerude
# 
#  1,4---1---1,5---1---1,6
#   |    |    |    |    |
#   4----x----5----x----6
#   |    |    |    |    |
#  2,4---2---2,5---2---2,6
#   |    |    |    |    |
#   4----x----5----x----6
#   |    |    |    |    |
#  3,4---3---3,5---3---3,6
#
# 
# 
# 
# 
# 
# #
for i in range(5):
    letcheck1[0,i]=final_words[0]
    letcheck1[2,i]=final_words[1]
    letcheck1[4,i]=final_words[2]
    letcheck2[i,0]=final_words[3]
    letcheck2[i,2]=final_words[4]
    letcheck2[i,4]=final_words[5]

newfinalword=final_words

letcheck=letcheck1+letcheck2
print(letcheck)





import random

# Initial 5x5 grid with empty spots at (1,1), (3,3), (1,3), and (3,1)
newgrid = np.copy(state_grid)

# Extract all non-empty letters
letters = [newgrid[i,j] for i in range(5) for j in range(5) if (i, j) not in [(1, 1), (3, 3), (1, 3), (3, 1),(0,0)]]



# Shuffle the list of letters 4 time to get some results since single shuffling leads to 
random.shuffle(letters)
random.shuffle(letters)
random.shuffle(letters)
random.shuffle(letters)

print(state_grid)
# Place the shuffled letters back, ensuring empty spots stay empty
index = 0
for i in range(5):
    for j in range(5):
        if (i, j) not in [(1, 1), (3, 3), (1, 3), (3, 1),(0,0)]:
            newgrid[i,j] = letters[index]
            index += 1

## Code for updating letcheck to keep a tab on what has been solved 
# so that if letter belongs to certain row /col and if they are in right row or col
# then they have blue color.
# 

newfinalword=final_words


# function to remove letter from the letcheck
def modifynewword(i,j,lett):
    if (i in [0,2,4]) and (j in [0,2,4]):
        r1=i//2
        c1=j//2+3
        newfinalword[r1]=newfinalword[r1].replace(lett,'',1)
        newfinalword[c1]=newfinalword[c1].replace(lett,'',1)
    elif ((i%2==0) and (j%2==1)):
        r1=i//2
        newfinalword[r1]=newfinalword[r1].replace(lett,'',1)
    elif ((j%2==0) and (i%2==1)):
        c1=j//2+3
        newfinalword[c1]=newfinalword[c1].replace(lett,'',1)
nnewfinalword=newfinalword

#function to rebuild letcheck
def buildfinal(r,c,lett):
    modifynewword(r,c,lett)
    for i in range(5):
        letcheck1[0,i]=newfinalword[0]
        letcheck1[2,i]=newfinalword[1]
        letcheck1[4,i]=newfinalword[2]
        letcheck2[i,0]=newfinalword[3]
        letcheck2[i,2]=newfinalword[4]
        letcheck2[i,4]=newfinalword[5]
    flc=letcheck1+letcheck2
    return flc




letcheck=letcheck1+letcheck2

@app.route("/")
def main():
    return render_template('index.html')

# REST api request to check if letter which is updated on a particular grid is correct or in some row or col which is correct
#   1: Correct Letter
#   2: Letter in right row or col or both
#   0: None of the above
# This will be request 
# #
@app.route("/correct/<letter>/<int:first>/<int:second>")
@cross_origin()
def read_item(letter,first,second):
    global letcheck
    print('mainletcheck')
    print(letcheck)
    if(state_grid[first-1][second-1]==letter):
        response = jsonify({"letter":1})
        print(letcheck)
        letcheck=buildfinal(first-1,second-1,letter)
        print(letcheck)
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



if __name__ == "__main__":
    app.run()
