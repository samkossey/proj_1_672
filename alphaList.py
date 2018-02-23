#INDEXED ALPHABET
# alphaList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# alphaDict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}

#SHIFT CIPHER
# for i in range(26):
#     answer = ""
#     for c in cipher:
#         p = alphaList[((alphaDict[c] + i) % 26)]
#         answer = answer + p
#     print "ANSWER with " + str(i) + "\n"
#     print answer

#NORMAL FREQUENCIES
normal_freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}

#SHIFTING
def shiftBy(c, n):
    return chr(((ord(c) - ord('a') + n) % 26) + ord('a'))

#FREQUENCY
def findFreq(filename):
    ch = file(filename,'r')
    cipher = ch.read()
    ch.close()
    frequency = {}
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(cipher.count(chr(ascii)))/len(cipher)

    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr]

    print "Should be near .065 if plain: " + str(sum_freqs_squared)
    
def findKey(filename):
    ch = file(filename,'r')
    cipher = ch.read()
    ch.close()
    keylist = []
    for k in range(1,300):
        subcipher = cipher[3::k]
        frequency = {}
        for ascii in range(ord('a'), ord('a')+26):
            frequency[chr(ascii)] = float(subcipher.count(chr(ascii)))/len(subcipher)

        sum_freqs_squared = 0.0
        for ltr in frequency:
            sum_freqs_squared += frequency[ltr]*frequency[ltr]
        if abs(sum_freqs_squared - .065) < .007:
            print "key: ", k, "freq: ", sum_freqs_squared
            keylist.append(k)
    findShift(cipher, keylist)
            # flag = False
            # for l in range(k):
            #     if flag:
            #         break
            #     subcipher = cipher[l::k]
            #     frequency = {}
            #     for ascii in range(ord('a'), ord('a')+26):
            #         frequency[chr(ascii)] = float(subcipher.count(chr(ascii)))/len(subcipher)

            #     sum_freqs_squared = 0.0
            #     for ltr in frequency:
            #         sum_freqs_squared += frequency[ltr]*frequency[ltr]
            #     if abs(sum_freqs_squared - .065) > .01:
            #         flag = True
            # if not flag:
            #     print k
            
def findShift(cipher, kl):
    # ch = file(filename,'r')
    # cipher = ch.read()
    # ch.close()
    
    #for key in kl:
    for key in kl:
        subcipher = cipher[3::key]
    
        frequency = {}
        for ascii in range(ord('a'), ord('a')+26):
            frequency[chr(ascii)] = float(subcipher.count(chr(ascii)))/len(subcipher)
    
        for possible_key in range(1, 26):
            sum_f_sqr = 0.0
            for ltr in normal_freqs:
                caesar_guess = shiftBy(ltr, possible_key)
                sum_f_sqr += normal_freqs[ltr]*frequency[caesar_guess]
            if abs(sum_f_sqr - .065) < .015:
                print "Key is probably: ", possible_key, " f_sqr is ",sum_f_sqr, " distance: ", key
    
def vingerize(cipher, kl, key):
    ch = file('ch2.txt','r')
    cipher = ch.read()
    ch.close()
    onlyletters = filter(lambda x: x.isalpha(), cipher)
    cipher = onlyletters.lower()
    answer = ""
    for i in range(len(cipher)):
        pos = i % kl
        answer = answer + str(shiftBy(cipher[i],-1*(ord(key[pos])-ord('a'))))
    print answer
    
def findShiftKey(key, filename):
    ch = file(filename,'r')
    cipher = ch.read()
    ch.close()
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
                print "Key is probably: ", possible_key, " f_sqr is ",sum_f_sqr, " distance: ", key, "pos: ", k
                sum_a = sum_a + sum_f_sqr
                count = count + 1
    if count > 0:
        print "AVR = ", sum_a/count, "KEY = ", key

def findKeywSpaces(filename):
    ch = file(filename,'r')
    cipher = ch.read()
    ch.close()
    for k in range(1,50):
        findShiftKey(k, filename)
        
#findKeywSpaces("ch2.txt")

#findKey("ch2.txt")

findShiftKey(16, "ch2.txt")

#findFreq("ch3.txt")
#findFreq("ch4.txt")

#vingerize("", 16, "coketurkgxwrsczo")

#look at 2 3 and 4

#2
#8 13 17 18 20 22 24 26 42

#8 poss .057
#17 .052
#18 .052
#20 .055
#22 .054
#24 .056
#26 .053
#42 .055

#16 ch2?

#2 14 10 4 19 20 17 10 6 23 22 17 18 2 25 14 
#c o k e t u r k g x w r s c z o

