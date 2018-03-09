import operator

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
    
#SUBSTITUTE
def substitute(cipher, subMap):
    answer = ""
    tempDict = {}
    tempVals = []
    tempKeys = []
    keys = subMap.keys()
    vals = subMap.values()
    skips = []
    bestScore = 0
    #check frequencies
    oneLetter = oneFreq(cipher)
    #sort frequencies
    sorted_oneLetter = sorted(oneLetter, key=oneLetter.get, reverse=True)
    print sorted_oneLetter
    for o in oneLetter:
        if oneLetter[o] == 0:
            skips.append(o)
    #lists of which letters still need assignments
    for ascii in range(ord('a'), ord('a')+26):
        ascii = chr(ascii)
        if ascii not in vals:
            tempVals.append(ascii)
        if ascii not in keys:
            if ascii not in skips:
                tempKeys.append(ascii)
    #iterate through cipher letters still in need of assignments
    for key in sorted_oneLetter:
        bestV = ""
        bestK  = ""
        k = ""
        if key in tempKeys:
            k = key
        else:
            continue
        answer = ""
        #add established substitutions
        for c in cipher:
            if ord(c) < 97:
                char = c
            elif c in keys:
                char = subMap.get(c)
                char = char.upper()
            elif (c in tempDict.keys()):
                char = tempDict.get(c)
                char = char.upper()
            else:
                char = c
            answer = answer + char
        cipher = answer
        print "\n"
        print cipher.lower()
        print tempDict
        print bestScore
            
        bestScore = 0
        #find which remaining substitution produces the best english score
        #for the corresponding cipher letter
        for v in tempVals:
            answer = ""
            for c in cipher:
                if (c == k):
                    char = v
                else:
                    char = c
                answer = answer + char
            tempScore = englishScore(answer.lower())
            if tempScore > bestScore:
                bestScore = tempScore
                bestV = v
                bestK = k
        #add the best pair to the list of substitutions
        tempDict[bestK] = bestV
        tempVals.remove(bestV)
        tempKeys.remove(bestK)
    answer = ""
    #final substitution with full list
    for c in cipher:
        if ord(c) < 97:
            char = c
        elif c in keys:
            char = subMap.get(c)
            char = char.upper()
        elif (c in tempDict.keys()):
            char = tempDict.get(c)
            char = char.upper()
        else:
            char = c
        answer = answer + char
    cipher = answer
    print cipher.lower()
    print tempDict
    for key,value in tempDict.items():
        subMap[key] = value
    return subMap
                
        
        
#PRINTING CURRENT ANSWER
def finalSub(cipher,subMap):
    answer = ""
    for c in cipher:
        char = subMap.get(c,c)
        answer = answer + char
    return answer

#WINNER
#subMap = {'y':'e', 'n': 't', 'q': 'h', 'v': 's', 'o':'g','r':'n', 'e':'i', 'p':'a', 'x':'d','a':'o','d':'r', 'z':'f','u':'m', 'j':'p','l':'u','g':'l','b':'k','c':'v','h':'w','t':'y','s':'b','f':'c'}
subMap = {'y':'e', 'n': 't', 'q': 'h','v':'s','p':'a','e':'i','r':'n','j':'p','t':'y'}
print substitute(readCipher('ch4.txt'), subMap) 
#print finalSub(readCipher('ch4.txt'), subMap) 

