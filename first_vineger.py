

"""
    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    ---------------------------------------------------
A   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
B   B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
C   C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
D   D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
E   E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
F   F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
G   G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
H   H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
I   I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
J   J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
K   K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
L   L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
M   M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
N   N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
O   O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
P   P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
Q   Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
R   R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
S   S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
T   T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
U   U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
V   V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
W   W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
X   X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
Y   Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
Z   Z A B C D E F G H I J K L M N O P Q R S T U V W X Y
"""


import math, pprint, string

table = []

# Intiialise table
start_char = 0
for x in range(0, 27):
    row = [ x % 26 for x in range(start_char, start_char+26) ]
    start_char += 1
    table.append(row)

# for row in table:
#     print(row)

def get_int(char):
    return ord(char.upper()) - 65

def get_chr(int):
    return chr(int + 65)

# get_int('A')
# get_int('B')
# get_chr(1)
# get_chr(2)


def apparitions(chaine):
    app = [0] * 26
    for c in chaine.upper():
        if c in string.ascii_uppercase:
            app[ord(c) - ord('A')] += 1
    return app

def ic(str):
    app = apparitions(str)
    s = sum (n*(n-1) for n in app)
    somme = sum(app)
    return s / (somme*(somme-1))

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def chi_squared(phrase):

    # this works as well as the practical cryptography example

    phrase = phrase.replace(' ', '').upper()
    expected = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,
                0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978,
                0.02360, 0.00150, 0.01974, 0.00074]

    total = 0
    counts = [0 for i in range(0, 26)]
    for char in phrase:
        counts[get_int(char)] += 1
        total += 1

    # Chi squared against english distribution
    sum1 = 0
    for i, count in enumerate(counts):
        sum1 += (  (count - (total * expected[i]))**2  ) / (  total*expected[i]  )

    return sum1




def vigenere_crack(ciphertext):
    TRIAL_KEY = ""
    # Assume len(key) == 2 first
    key_len = 2
    max_len = 15

    # CVa;culate trials by creating different strings to evaluate using the IC and log the ic results in trials
    trials = []
    for length in range(key_len, max_len + 1):
        for run in range(1, length + 1):
            # print("If key were len", length)
            # print("Sequence", run)
            cc = run - 1
            st = ""
            while cc <= len(ciphertext) - 1:
                # print(ciphertext[cc], end="")
                st += ciphertext[cc]
                cc += length
            # print(st, f"({ic(st)}")
            trials.append([length, run, st, ic(st)])

    # pprint.pprint(trials)

    # Here we find the trial with the highest average IC value, this is the most likely to be the period
    # Once we have that, we take the string from that recurrent key length
    averages = {}
    for length in range(key_len, max_len + 1):
        m = str(round(mean([x[3] for x in trials if x[0] == length]), 3))
        if m in averages:
            averages[m].append(length)
        else:
            averages[m] = [length]
    print("keys", averages.keys())
    smallest_key = min(averages[str(max([ float(x) for x in averages.keys()] ))])
    print("smallest_key:", smallest_key)
    print("averages:", averages)
    test_str = "".join([x for (i, x) in enumerate(ciphertext) if i % smallest_key == 0])
    print("Test String:", test_str)

    # Test deciphering and have a squiz for the lowest chi-sq

    for i, trial in enumerate([ x for x in filter(lambda x: x[0] == 7, trials)]):
        lowest_chi = float('inf')
        chi_val = None
        for i in range(0, 26):
            s = ""
            for char in trial[2]:
                s += get_chr((get_int(char) - i) % 26) # TODO - Cant MOD here as the ascii stuff sits can I?
            # print(i, s, chi_squared(s))
            if lowest_chi > chi_squared(s):
                lowest_chi = chi_squared(s)
                chi_val = i

        # print(chi_val, lowest_chi)

        TRIAL_KEY += get_chr(chi_val)
        print(TRIAL_KEY)


    # Got the chi value thats lowest, it gave us 2, which is C (ABC)
    # Now we need to do this again for the other string up until length 7, len 7 because we identified it as the period






vigenere_crack("vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmumshwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluysdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt")
print("\n")
with open('ciphertext.txt') as cipher_file:
    ct = cipher_file.read().replace(" ", "").replace(",", "").replace(".", "").lower().strip('\n')
    vigenere_crack(ct)