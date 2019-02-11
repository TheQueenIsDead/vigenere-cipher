import itertools
import pprint
import re
from functools import reduce
from itertools import permutations

import freqAnalysis
from vigenere import Vigenere
# https://inventwithpython.com/hacking/chapter21.html



class Kasiski():

    def __init__(self):
        self.v = Vigenere()


    def set_ct(self, ct):
        # Make sure ct is only alphanumeric
        filter_re = re.compile('[^a-zA-Z]')
        self.ct = filter_re.sub('', ct).upper()

    # def isRepeating(self, substr):
    #
    #     index = self.ct.find(substr)
    #     if index == -1:
    #         return False
    #     else:
    #         # Search rest of the string
    #         second = self.ct[index+len(substr):].find(substr)
    #         if second != -1:
    #             print(f"Found {substr} at {index}, and {second}")

    def findPeriod(self):

        d = {}

        # max_len = len(self.ct)
        max_len = 3

        for length in range(2, max_len + 1):

            cc = 0
            while cc < len(self.ct):
                # print(self.ct[cc:cc+length])
                substr = self.ct[cc:cc+length]
                if len(substr) > 2:
                    # self.isRepeating(substr)
                    if substr in d:
                        d[substr]['count'] += 1
                        d[substr]['indexes'].append(cc)
                    else:
                        d[substr] = {
                            "substr": substr,
                            "count": 1,
                            "indexes": [cc]
                        }
                cc += 1

        # Getting the spaces
        # print(d.values())
        # pprint.pprint(list(permutations([x['indexes'] for x in filter(lambda x: x['count'] > 1, d.values())])))
        l = [x for x in filter(lambda x: x['count'] > 1, d.values())]

        for item in l:


            # print("Indexes:", item['indexes'])

            # Old incorrect version
            # item['spaces'] = []
            # i, j = 0, 1
            # while i < len(item['indexes']):
            #     if j >= len(item['indexes']):
            #         item['spaces'].append(item['indexes'][0] - item['indexes'][i])
            #     # print(item['substr'], ":", item['indexes'][i], item['indexes'][j], item['indexes'][j] - item['indexes'][i])
            #     else:
            #         print(len(item['indexes']), i, j)
            #         item['spaces'].append(item['indexes'][j] - item['indexes'][i])
            #     i, j = i + 1, j + 1

            i = 0
            item['spaces'] = []
            while i < len(item['indexes']):
                for index in item['indexes'][i + 1:]:
                    item['spaces'].append(index - item['indexes'][i])
                i += 1

        return l

    def spacingFactors(self, space_list):
        """
        Gets the factors of all of the spaces and counts their occurences.
        Returns a list of the most occuring factors, these are the most likely
        to be the correct key length
        :param space_list:
        :return:
        """

        factors = []

        def reduce_arr(a, b):
            return a + b

        new_arr = reduce(reduce_arr, [x['spaces'] for x in space_list])

        for n in set([x for x in new_arr]):
            curr_factors = []
            for i in range(1, n):
                if i not in curr_factors:
                    for j in range(1, n+1):
                        if i*j == n:
                            # print(f"Found {i} and {j} for {n}")
                            curr_factors.append(i)
                            curr_factors.append(j)
            factors += curr_factors

        factor_count = {}
        for x in factors:
            if x in factor_count:
                factor_count[x] += 1
            else:
                factor_count[x] = 1

        del factor_count[1] # Trivial and not useful

        pprint.pprint(factor_count)

        # Print and return highest likelihood
        max_freq = max([v for (k, v) in factor_count.items()])

        # print(max_freq)

        highest = [ k for (k, v) in factor_count.items() if v == max_freq]

        # print("Highest:", highest)

        return sorted(highest)

    def getNthLetters(self, n):

        n_strings = []

        for i in range(0, n):
            # For every starting pos

            s = ""
            cc = i
            while cc < len(self.ct):
                s += self.ct[cc]
                cc += n
            n_strings.append(s)

        return n_strings

    def cycleDecypher(self, ciphertext):
        """
        Technically this function decrypts the cipher as it's akin to a ceaser cipher to a degree.
        Returns a list of all possibilities for a key in the a-z range
        :param ciphertext:
        :return:
        """

        most_probable = []
        highest = float('-inf')
        for i in range(0, 26):
            s = ""
            for char in ciphertext:
                s += self.v.get_chr((self.v.get_int(char) - i) % 26)
            most_probable.append((self.v.get_chr(i), s, freqAnalysis.englishFreqMatchScore(s)))
            highest = max(highest, freqAnalysis.englishFreqMatchScore(s))

        return [ x for x in most_probable if x[2] == highest]

    def brute_force(self, possible_keys):
        char_arrays = [[y[0] for y in x] for x in possible_keys]
        print(char_arrays)


        # for s in char_arrays:
        #     for c in s:
        #         self.brute_layer(char_arrays, c, )

        #
        # results = []
        #
        # print("Easy:", list(itertools.product(char_arrays[0], char_arrays[1])))
        # print()
        #

        print("Starting brute...")
        i, j = 1, 2
        res = list(itertools.product(char_arrays[0], char_arrays[1]))
        while j < len(char_arrays):
            res = list(itertools.product(res, char_arrays[j]))
            i, j = i + 1, j + 1


        def unwrap(values):

            if isinstance(values[0], str) and isinstance(values[1], str): # Base case of two ints
                return [values[1], values[0]]

            res = [values[-1]]
            res += unwrap(values[0])
            return res

        possible_keys = []
        for tuple_set in res:
            # print(tuple_set)
            possible_keys.append("".join(reversed(unwrap(tuple_set))))

        return possible_keys

k = Kasiski()

print("Ciphertext:")
k.set_ct("Ppqca xqvekg ybnkmazu ybngbal jon i tszm jyim. Vrag voht vrau c tksg. Ddwuo xitlazu vavv raz c vkb qp iwpou.")
print(k.ct)

print("Periods:")
periods = k.findPeriod()
pprint.pprint(periods)

print("Factors:")
factors = k.spacingFactors(periods)
print(factors)


# Proper, but we'll only work with 4 for the current moment
# print("Get N Letters:")
# for length in factors:
#     n_strings = k.getNthLetters(length)
#     pprint.pprint(n_strings)


print("Get N Letters:")
n_strings = k.getNthLetters(4) # Because 4 is returned in the above example, refer to above for proper stuff
pprint.pprint(n_strings)

print("Cycling:")
possible_keys = []
for i, s in enumerate(n_strings): # TODO - Remove [:1] from here, once again limiting for the example
    print(f"The most likely keys for string {i} are:")
    i_keys = k.cycleDecypher(s)
    possible_keys.append(i_keys)
    pprint.pprint([x[0] for x in i_keys])

print("Brute forcing")
print(k.brute_force(possible_keys))





