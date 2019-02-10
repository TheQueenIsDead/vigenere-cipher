'''
Allows scoring of text using n-gram probabilities
17/07/12
'''
from math import log10

class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        with open(ngramfile, 'r') as ngram:
            for line in ngram.readlines():
                key,count = line.split(sep)
                self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor
        return score

fitness = ngram_score('english_quadgrams.txt')
print(fitness.score('ATTACK THE EAST WALL OF THE CASTLE AT DAWN'))


key_len = 7

key = "A" * 7

# A is 1

# For every character in the key
for i in range(0, key_len):
    print(i)

    # Cycle the char through 26 letters assessing the fitness
    results = []
    for char in range(0, 25):
        up_cycled_char = chr(  ((ord(key[i].upper()) - 64) + 1) + 64)
        key = key[:i] + up_cycled_char + key[i+1:] # Up to current cycler, plus newly cycled char, plus rest

        #decipher text with key

        #print decipherd score with key
        print(key, fitness.score(key))



print(ord('A'))