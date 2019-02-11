import math

class Vigenere():

    def __init__(self):

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

        ciphertext = ""
        for i, char in enumerate(plaintext):
            ciphertext += self.get_chr(self.table[self.get_int(char)][self.get_int(key[i])])
        return ciphertext

    def decrypt(self, ciphertext):

        ciphertext = ciphertext.replace(' ', '').upper()

        if len(ciphertext) > len(self.key):
            multiplier = math.ceil(len(ciphertext) / len(self.key))
            key = self.key * multiplier
        key = key[:len(ciphertext)]

        plaintext = ""
        for i, c in enumerate(ciphertext):
            row = self.table[self.get_int(key[i])]
            plaintext += self.get_chr(row.index(self.get_int(c)))

        return plaintext


k = "FORTIFICATION"
pt = "DEFENDTHEEASTWALLOFTHECASTLE"
ct = "ISWXVIBJEXIGGBOCEWKBJEVIGGQS"

v = Vigenere()
v.set_key(k)

assert v.key == "FORTIFICATION"
assert v.encrypt(pt) == ct
assert v.decrypt(ct) == pt