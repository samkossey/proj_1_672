import operator
import random
import math
import copy

#READING IN FILE
def readCipher(filename):
    ch = file(filename,'r')
    cipher = ch.read()
    onlyletters = filter(lambda x: x.isalpha(), cipher)
    cipher = onlyletters.lower()
    ch.close()
    return cipher
    
#SUM FREQ SQUARED
def findFreq(cipher):
    frequency = {}
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(cipher.count(chr(ascii)))/len(cipher)

    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr]
      
    return sum_freqs_squared

#LETTER FREQUENCIES
def twoFreq(cipher):
    frequency = {}
    c = 0
    while c < (len(cipher)-1):
        if cipher[c]+cipher[c+1] not in frequency.keys():
            frequency[cipher[c]+cipher[c+1]] = float(cipher.count(cipher[c]+cipher[c+1]))/len(cipher)
        c = c+2
    return frequency
    
#QUADGRAM FREQ MAP
def quadgrams():
    qgrams = {}
    for line in file('quadgrams.txt'):
        key,count = line.split(' ')
        qgrams[key] = int(count)
    total = sum(qgrams.itervalues())
    for k in qgrams.keys():
        qgrams[k] = math.log10(float(qgrams[k])/total)
    floor = math.log10(.01/total)
    return floor,qgrams
    
#QGRAM SCORE
def qgramScore(text,floor,qgrams):
    score = 0
    for c in range(len(text)-4+1):
        if text[c:c+4].upper() in qgrams:
            
            score = score + qgrams[text[c:c+4].upper()]
        else:
            score = score + floor
    return score
    
#ENGLISH SCORE
def englishScore(text):
    f=file('most_common_words.txt', 'r')
    words = [word.strip() for word in f]
    f.close()
    length = len(text)
    factor = 1
    freq = findFreq(text)
    if (freq - .065) < .005:
        factor = 2
    score = 0.0
    for w in words:
        if len(w) > 1:
            tally = text.count(w)
            if len(w) >= 3:
                tally = tally * 3
            score = score + tally
    score = score / (length/5)
    score = score * factor
    return score
    
#LETTERS <--> NUMBERS
def toNumber(char):
    return (ord(char) - 97)
    
def toChar(num):
    return chr(num + 97)
    
#DECRYPT WITH KNOWN KEY
def decryptPlay(cipher, key):
    c = 0
    final = ""
    while (c<len(cipher)-1):
        pos1 = findLetter(cipher[c],key)
        pos2 = findLetter(cipher[c+1],key)
        final1 = ""
        final2 = ""
        if (pos1[0] == pos2[0]):
            final1 = key[pos1[0]][pos1[1]-1%5]
            final2 = key[pos2[0]][pos2[1]-1%5]
        elif (pos1[1] == pos2[1]):
            final1 = key[pos1[0]-1%5][pos1[1]]
            final2 = key[pos2[0]-1%5][pos2[1]]
        else:
            final1 = key[pos1[0]][pos2[1]]
            final2 = key[pos2[0]][pos1[1]]
        final = final + final1 + final2
        c = c+2
        
    return final
        
#FIND LETTER IN KEY
def findLetter(l, key):
    for i in range(5):
        for j in range(5):
            if key[i][j] == l:
                return (i,j)

#GENERATE A RANDOM KEY TO USE IN SA HILL CLIMB        
def generateKey():
    pList = range(26)
    random.shuffle(pList)
    current = 0;
    key = [[toChar(1)]*5 for i in range(5)]
    for i in range(5):
        for j in range(5):
            if pList[current]==9:
                current = current + 1;
            key[i][j] = toChar(pList[current])
            current = current + 1;
    return key

#SWAP TWO RANDOM LETTERS IN KEY FOR SA HILL CLIMB    
def switchKey(key):
    r1 = random.randint(0,4)
    c1 = random.randint(0,4)
    r2 = random.randint(0,4)
    c2 = random.randint(0,4)
    temp = key[r1][c1]
    temp2 = key[r2][c2]
    key[r1][c1] = temp2
    key[r2][c2] = temp
    return key
    
#SA HILL CLIMBING
#for best results, high temp, low step, high count
def saHill(cipher):
    #generate the quadgram map
    floor,qgrams = quadgrams()
    #random starting key
    parent = generateKey()
    #quad score of starting key
    fitness = qgramScore(decryptPlay(cipher,parent),floor,qgrams)
    temp = 20
    step = .9
    #to keep track of what iterations you're on (check progress)
    fh = open('count_play.txt','w')
    
    #decrement temp by the step
    while (temp > 1):
        count = 50000
        while (count > 0):
            fh.write(str(temp)+ ", " + str(count) + "\n")
            tempParent = copy.deepcopy(parent)
            #create a child with two swapped letters
            child = switchKey(tempParent)
            childFit = 0
            childFit = qgramScore(decryptPlay(cipher,child),floor,qgrams)
            dF = abs(abs(childFit) - abs(fitness))
            #check if the child fitness is better
            if (childFit > fitness):
                #if child fitness is better choose it over parent
                parent = child
                fitness = childFit
            else:
                #if not use their difference in magnitude and your
                #current temp to generate a probability
                #switch if random number is within that probability
                #(prevents getting stuck in local min/max)
                #as temp gets lower, you are less likely to switch to child
                #if different in magnitude is small more likely to switch
                prob = round(math.e**(-1*dF/temp),10)
                r = random.random()
                if (prob > r):
                    parent = child
                    fitness = childFit
            count = count - 1
        temp = temp - step
        
    theAnswer = decryptPlay(cipher, parent)
    print "QSCORE: ", qgramScore(theAnswer,floor,qgrams)
    fh.write(theAnswer + "\n")
    for i in range(5):
        for j in range(5):
            fh.write(parent[i][j] + ", ")
        fh.write("\n")
    fh.close()
    print theAnswer
    print parent
    return theAnswer
    

#saHill(readCipher('ch1.txt'))    
#WINNER
key = [['h', 'a', 'n', 'e', 'c'], ['s', 'f', 't', 'r', 'l'], ['p', 'i', 'm', 'o', 'd'], ['g', 'v', 'y', 'z', 'u'], ['b', 'k', 'q', 'w', 'x']]
print decryptPlay(readCipher('ch1.txt'),key)


