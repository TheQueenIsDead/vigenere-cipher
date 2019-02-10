
import math, pprint, string
import random


class Vigenere():

    def __init__(self):

        # self.key = "".join(random.randint(1000000, 9999999))
        # print(self.key)

        self.table = []

        # Intiialise table
        start_char = 0
        for x in range(0, 27):
            row = [x % 26 for x in range(start_char, start_char + 26)]
            start_char += 1
            self.table.append(row)

        self.get_int('A')
        self.get_int('B')
        self.get_chr(1)
        self.get_chr(2)

    def get_int(self, char):
        return ord(char.upper()) - 65

    def get_chr(self, int):
        return chr(int + 65)

    def set_key(self, k):
        self.key = k

    def encrypt(self, plaintext):


        plaintext = plaintext.replace(' ', '').upper()

        if len(plaintext) > len(self.key):
            multiplier = math.ceil(len(plaintext) / len(self.key))
            key = self.key * multiplier

        key = key[:len(plaintext)]
        print(key)
        print(plaintext)

        print("Cipher:")
        # print("".join([ table[get_int(char)][get_int(key[i])] for (i, char) in enumerate(plaintext) ]))
        for i, char in enumerate(plaintext):
            # print(i, char, ": ", key[i], get_int(key[i]))
            print(self.get_chr(self.table[self.get_int(char)][self.get_int(key[i])]), end="")
        print("")

    def decrypt(self, ciphertext):

        if len(ciphertext) > len(self.key):
            multiplier = math.ceil(len(ciphertext) / len(self.key))
            key = self.key * multiplier
        key = key[:len(ciphertext)]


        print("Decipher")
        for i, c in enumerate(ciphertext):
            row = self.table[self.get_int(key[i])]
            print(self.get_chr(row.index(self.get_int(c))), end="")
            cipher_index = None # Current cipher letter in the above row
            column = None # Index as above

            # Here the column is the actual a-z int val


            # we need to find the c in the row designated by key, and then fihure out the index as it will be the pt
        print("")


v = Vigenere();
v.set_key("FORTIFICATION")
v.encrypt("DEFENDTHEEASTWALLOFTHECASTLE")
v.decrypt("ISWXVIBJEXIGGBOCEWKBJEVIGGQS")

# vigenere_encrypt("FORTIFICATION", "DEFENDTHEEASTWALLOFTHECASTLE")
# vigenere_encrypt("defend the east wall of the castle", "fortification")
