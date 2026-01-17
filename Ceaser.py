class Caesar:
    def __init__(self, key):
        self.key = key % 26

    def encrypt(self, text):
        result = ""

        for c in text:
            if 'A' <= c <= 'Z':
                result += chr((ord(c) - 65 + self.key) % 26 + 65)
            elif 'a' <= c <= 'z':
                result += chr((ord(c) - 97 + self.key) % 26 + 97)
            else:
                result += c

        return result

    def decrypt(self, text):
        result = ""

        for c in text:
            if 'A' <= c <= 'Z':
                result += chr((ord(c) - 65 - self.key) % 26 + 65)
            elif 'a' <= c <= 'z':
                result += chr((ord(c) - 97 - self.key) % 26 + 97)
            else:
                result += c

        return result

    def brute_force(self, text):
        print("\nTrying all possible keys (Brute Force Caesar):\n")

        for k in range(26):
            temp = Caesar(k)
            print("Key", k, "=>", temp.decrypt(text))
