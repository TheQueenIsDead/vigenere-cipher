'''
Allows scoring of text using n-gram probabilities
17/07/12
'''
import pprint
from math import log10
from vigenere import Vigenere

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

# fitness = ngram_score('english_quadgrams.txt')
# print(fitness.score('ATTACK THE EAST WALL OF THE CASTLE AT DAWN'))
#
#
# def get_eval_text(index, ct, period):
#
#     index += 1 # We want count, not index
#
#     s = ""
#
#     cc = 0
#     while cc < len(ct):
#         s += ct[cc:cc+index]
#         cc += period
#
#     return s
#
# print(get_eval_text(3, "DEFERULHEEAWKOALLOJKZECASXCW", 7))
#
#
#
#
# # A is 1
#
# # For every character in the key
#
# v = Vigenere()
#
# ct = "FMULRULJMTHWKOCTAVJKZGKPZXCW"
# for k in range(3, 20):
#
#     key_len = 7
#     key = "A" * 7
#
#     for i in range(0, key_len):
#         # print(i)
#
#         # Cycle the char through 26 letters assessing the fitness
#         results = []
#         for char in range(0, 25):
#
#             # Test key
#
#             #decipher text with key
#             v.set_key(key)
#             # print(key, v.decrypt(ct), fitness.score(v.decrypt(ct)))
#
#             results.append({
#                 "score": fitness.score(get_eval_text(i, v.decrypt(ct), key_len)),
#                 "key": key,
#                 "decryption": v.decrypt(ct),
#                 "char": key[i]
#             })
#
#
#
#
#
#
#             # Cycle key for next loop
#             up_cycled_char = chr(  ((ord(key[i].upper()) - 64) + 1) + 64)
#             key = key[:i] + up_cycled_char + key[i+1:] # Up to current cycler, plus newly cycled char, plus rest
#
#         # After we have the results, lock the highest fitness index as the key
#         key = key[:i] + sorted(results, key=lambda x: x['score'], reverse=True)[0]['char'] + key[i+1:]
#
#         # pprint.pprint([ (x['char'], x['score']) for x in sorted(results, key=lambda x: x['score'], reverse=True)])
#     print(key)
#
#
#
#
#
# """
# we should only calculate fitness from the shaded parts of the decrypted text.
# This reduces the effect on the total fitness of the garbled text that is present due to unsearched components of the key.
#
# (If we're on the third letter, only search those initial letters every period of the test key)
#
# current key: CIPHAAACIPHAAACIPHAAACIPHAAA
#  ciphertext: FMULRULJMTHWKOCTAVJKZGKPZXCW
#   decrypted: DEFERULHEEAWKOALLOJKZECASXCW
#
#
#
#
#
# """