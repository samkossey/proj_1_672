#NORMAL FREQUENCIES
normal_freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}

#SHIFTING
def shiftBy(c, n):
    return chr(((ord(c) - ord('a') + n) % 26) + ord('a'))
    
#FREQUENCY
def findFreq(cipher):
    frequency = {}
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(cipher.count(chr(ascii)))/len(cipher)

    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr]
      
    return sum_freqs_squared

    
def _findPossKey(key, flag, cipher):
    sum_a = 0.0
    count = 0.0
    for k in range(key):
        subcipher = cipher[k::key]
    
        frequency = {}
        for ascii in range(ord('a'), ord('a')+26):
            frequency[chr(ascii)] = float(subcipher.count(chr(ascii)))/len(subcipher)
        for possible_key in range(1, 26):
            sum_f_sqr = 0.0
            for ltr in normal_freqs:
                caesar_guess = shiftBy(ltr, possible_key)
                sum_f_sqr += normal_freqs[ltr]*frequency[caesar_guess]
            if abs(sum_f_sqr - .065) < .014:
                sum_a = sum_a + sum_f_sqr
                count = count + 1
                if flag:
                    print "POS: ", k," SHIFT BY: ", possible_key, " FREQ: ", sum_f_sqr, " KEY: ", key
    if count > 0:
        if abs((sum_a/count) - .065) < .008:
            print "AVR = ", sum_a/count, "KEY = ", key
        
def findPossKey(cipher):
    for key in range(1,50):
        _findPossKey(key, False, cipher)
        
def readCipher(filename):
    ch = file(filename,'r')
    cipher = ch.read()
    onlyletters = filter(lambda x: x.isalpha(), cipher)
    cipher = onlyletters.lower()
    ch.close()
    return cipher
    
def vigenerize(cipher, kl, key):
    answer = ""
    for i in range(len(cipher)):
        pos = i % kl
        answer = answer + str(shiftBy(cipher[i],-1*(ord(key[pos])-ord('a'))))
    return answer
    
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
            if len(w) > 3:
                tally = tally * 3
            score = score + tally
    score = score / (length/5)
    score = score * factor
    return score
  
#1    
#find which key length is most likely
#findPossKey(readCipher('ch2.txt')) #16 gives the best average

#2
#picked shift that gave closest frequency for each
#with key in mind, output the likely shifts
#_findPossKey(16, True, readCipher('ch2.txt'))

#3
#2 14 10 4 19 20 17 10 6 23 22 17 18 2 25 14 
#c o k e t u r k g x w r s c z o

#4
#decrypt with the suspected key
plain = vigenerize(readCipher('ch2.txt'), 16, "coketurkgxwrsczo")
print plain
#5
#likelihood of being english score 
#at least over 15 should be pretty solid?
print englishScore(plain)


