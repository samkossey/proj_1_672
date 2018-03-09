import random
import re
import itertools
import math

digrams = ['th','he','in','er','an','re','ed','on','es','st','en','at','to','nt','ha','nd','ou', 'ea','ng','as', 'or','ti','is','et','it','ar','te','se','hi','of']

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
    
#BIGRAM FREQ MAP
def bigrams():
    bgrams = {}
    for line in file('bigrams.txt'):
        key,count = line.split(' ')
        bgrams[key] = int(count)
    total = sum(bgrams.itervalues())
    for k in bgrams.keys():
        bgrams[k] = math.log10(float(bgrams[k])/total)
    floor = math.log10(.01/total)
    return floor,bgrams
    
#BGRAM SCORE
def bgramScore(text,floor,bgrams):
    score = 0
    for c in range(len(text)-2+1):
        if text[c:c+2].upper() in bgrams:
            
            score = score + bgrams[text[c:c+2].upper()]
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
    
#FINDING NUMBER OF COLUMNS
#not helping, but wanted to look at word likelihoods in each
def findColNum(cipher, guess):
    size = len(cipher)/guess
    r = len(cipher)%guess
    c = 0
    pos = 0
    answer=""
    while c < guess:
        char = cipher[pos]
        c = c+1
        if r > 0:
            pos = pos + size + 1
            r = r-1
        else:
            pos = pos + size
        answer = answer + char
    print answer
    freq = findFreq(answer)
    print freq
    
def digramDiff(cipher, c1, c2, c3):
    c1_list = [m.start() for m in re.finditer(c1, cipher)]
    c2_list = [m.start() for m in re.finditer(c2, cipher)]
    c3_list = [m.start() for m in re.finditer(c3,cipher)]
    diff_list = []
    for ch1 in c1_list:
        for ch2 in c2_list:
            for ch3 in c3_list:
                if abs(ch1 - ch2)%(len(cipher)/8) == abs(ch1-ch3)%(len(cipher)/8) == abs(ch2-ch3)%(len(cipher)/8):
                    diff_list.append((ch1,ch2,ch3))
    
    checkDigrams(cipher, diff_list)

#trying to look for digrams in this    
def checkDigrams(cipher, diList):
    for d in diList:
        if (cipher[d[0]+1]+cipher[d[1]+1]) in digrams:
            if (cipher[d[1]+1]+cipher[d[2]+1]) in digrams:
                print d
                print cipher[d[0]:d[0]+6]
                print cipher[d[1]:d[1]+6]
                print cipher[d[2]:d[2]+6]
        
def findDigraph(cipher, c1, c2, cols):
    c1_list = [m.start() for m in re.finditer(c1, cipher)]
    c2_list = [m.start() for m in re.finditer(c2, cipher)]
    diList = []
    rowNum = len(cipher)/cols
    r = len(cipher)%cols
    for ch1 in c1_list:
        for ch2 in c2_list:
            diff = abs(ch2-ch1)
            if diff>=rowNum:
                if ((cipher[ch1+1])+(cipher[ch2+1])) in digrams:
                    if ((cipher[ch1+2])+(cipher[ch2+2])) in digrams:
                        if ((cipher[ch1+3])+(cipher[ch2+3])) in digrams:
                            diList.append((ch1,ch2))
    print diList
    for d in diList:
        print "DIGRAM", d
        print cipher[d[0]:d[0]+5]
        print cipher[d[1]:d[1]+5]
    
 
#could take 8,9,10 columns
    
print len(readCipher('ch5.txt'))%9

#saw that english is usually 40% vowels, didn't really help
def vowelCheck(cipher,cols):
    total = 0.0
    for i in range(cols):
        sub = cipher[i::(len(cipher)/cols)]
        vowelCount = sub.count('a') + sub.count('e') + sub.count('i') + sub.count('o') + sub.count('u')
        freq = float(vowelCount) / len(sub)
        total = total + freq
    print total/cols

def col_trans(plain):
    cols = random.randint(3,3)
    key = range(cols)
    random.shuffle(key)
    return "".join(plain[i::cols].lower() for i in key), key
    
#tried an 8 column brute force (don't know if it's actually 8)
#also struggling because the no padding really throws things off
#(my cipher isn't divisible by 8,9,or 10 unfortunately)
def bruteCol(cipher):
    cList = list(itertools.permutations([0,1,2,3,4,5,6,7]))
    test = cipher[::73]
    bestString = ""
    bestScore = 0
    for zero,one,two,three,four,five,six,seven in cList:
        final = ""
        score = 0
        final += test[zero]
        final += test[one]
        final += test[two]
        final += test[three]
        final += test[four]
        final += test[five]
        final += test[six]
        final += test[seven]
        score = englishScore(final)
        if (score > bestScore):
            bestScore = score
            bestString = final
    print bestScore
    print bestString
        
        
    
# #test = col_trans("himynameissam")
# test = "hellothere"
# print test[1::2]
# cipher = readCipher('ch5.txt')
#bruteCol(cipher)
#findColNum(readCipher('ch5.txt'), 9)
#print findFreq(readCipher('ch5.txt'))
#digramDiff(readCipher('ch5.txt'),'t','h','e')
#findDigraph(readCipher('ch5.txt'),'t','h',8)
#english score 11 of original
#print englishScore(readCipher('ch5.txt')) 
#vowelCheck(readCipher('ch5.txt'), 10)