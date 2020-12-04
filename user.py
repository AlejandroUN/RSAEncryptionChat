from rsa import rsa


class user:


    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = rsa.findN(self,p,q)
        self.totient = rsa.findTotient(self, p, q)
        self.e = rsa.findTotientCoprime(self, self.totient)
        self.d = rsa.findInverse(self, self.e, self.totient)

    def sendMessage(self, message):
        return rsa.codificateMessage(self, self.n, self.e, message)

    def receiveMessage(self, message):
        return rsa.decodeMessage(self, self.n, self.d, message)

    def test(self):
        return rsa.findN(self,3,11)

    def getN(self):
        return self.n

if __name__ == "__main__":
    gg = user(3,11)

    print(gg.sendMessage("hola"))
    print(gg.receiveMessage(gg.sendMessage("hola")))