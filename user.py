from RSA import RSA


class User:

    def __init__(self):
        self.p = p
        self.q = q
        self.n = RSA.find_n(self,p,q)
        self.totient = RSA.find_totient(self, p, q)
        self.e = RSA.find_totient_coprime(self, self.totient)
        self.d = RSA.find_inverse(self, self.e, self.totient)
        self.public_key = (n, e)

    def send_message(self, message):
        return RSA.codificate_message(self, self.n, self.e, message)

    def receive_message(self, message):
        return RSA.decode_message(self, self.n, self.d, message)

    def test(self):
        return RSA.find_n(self,3,11)

    def get_n(self):
        return self.n

if __name__ == "__main__":

    gg = User(3,11)

    print(gg.send_message("hola"))
    print(gg.receive_message(gg.send_message("hola")))