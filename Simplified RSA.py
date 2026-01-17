class RSA_manager():
    def __init__(self):
        self.N = 1000609937
        self.e = 17
        self.__d = 176558813

    def encrypt_rsa(self, other, message):
        m = int(message)
        c = pow(m, other.e, other.N)
        return c

    def decrypt_rsa(self, c):
        m = pow(int(c), self.__d, self.N)
        return str(m)
