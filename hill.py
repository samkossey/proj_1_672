import operator
import itertools

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
def oneFreq(cipher):
    frequency = {}
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(cipher.count(chr(ascii)))/len(cipher)
    return frequency
    
def twoFreq(cipher):
    frequency = {}
    for ascii1 in range(ord('a'), ord('a')+26):
        for ascii2 in range(ord('a'), ord('a')+26):
            frequency[chr(ascii1)+chr(ascii2)] = float(cipher.count(chr(ascii1)+chr(ascii2)))/len(cipher)
    return frequency
    
def threeFreq(cipher):
    frequency = {}
    for ascii1 in range(ord('a'), ord('a')+26):
        for ascii2 in range(ord('a'), ord('a')+26):
            for ascii3 in range(ord('a'), ord('a')+26):
                if cipher.count(chr(ascii1)+chr(ascii2)+chr(ascii3)) > 2:
                    frequency[chr(ascii1)+chr(ascii2)+chr(ascii3)] = float(cipher.count(chr(ascii1)+chr(ascii2)+chr(ascii3)))/len(cipher)
    return frequency
    


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
    
#GENERATE MATRICES
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def hill(cipher):
    list_a = list(range(26))
    matrixList = list(itertools.product(list_a, repeat =4))
    print len(matrixList)
    bestScore = 0
    bestA = ""
    bestB = ""
    bestC = ""
    bestD = ""
    count = 0
    fh = open('count.txt','w')
    for one,two,three,four in matrixList:
        fh.write(str(count) + "\n")
        count = count + 1
        tempScore = 0
        a = one
        b = two
        c = three
        d = four
        det = (a*d - b*c) % 26
        det2 = ((a-1)*d - b*(c-1)) % 26
        if (det % 2 != 0 )and (det % 13 != 0) and (det2 % 26 != 0):
            tempScore = decryptHill(cipher, a, b, c, d)
            if (tempScore > bestScore):
                bestScore = tempScore
                bestA = a
                bestB = b
                bestC = c
                bestD = d
        else:
           continue
    fh.close()
    print bestScore, bestA, bestB, bestC, bestD
       
#DECRYPT
def decryptHill(cipher, a, b, c, d):
    index = 0
    answer = ""
    while (index != len(cipher)):
        c1 = toNumber(cipher[index])
        c2 = toNumber(cipher[index+1])
        p1 = toChar((a*c1 + b*c2)%26)
        p2 = toChar((c*c1 + d*c2)%26)
        answer = answer + p1 + p2
        index = index + 2
    print answer
    print englishScore(answer)
    return englishScore(answer)
        
        
#LETTERS --> NUMBERS
def toNumber(char):
    return (ord(char) - 97)
    
def toChar(num):
    return chr(num + 97)
    
# freq = twoFreq(readCipher('ch3.txt'))
# sorted_freq = sorted(freq, key=freq.get, reverse=True)
# for f in sorted_freq:
#     if freq[f] == 0:
#         continue
#     print f, freq[f]

#hill(readCipher('ch3.txt'))

decryptHill("dhixbv",14,11,1,15)