class rsa:

    def findN(self, p, q):
        return p*q

    def findTotient(self, p, q):
        return ((p-1)*(q-1))

    def findTotientCoprime(self, totient):
        for x in range(totient):
            if self.findHCFWithEuclidsAlgorithm(x+1,totient) == 1:
                return (x+1)
        return 0

    def findHCFWithEuclidsAlgorithm(self, a, b):
        if a%b == 0:
            return b
        else:
            return self.findHCFWithEuclidsAlgorithm(self, a, a%b)

    def findInverse(self, e, totient):
        for x in range(totient-1):
            if ((e*(x+1))%totient) == 1:
                return (x+1)
        return 0

    def codificateMessage(self, n, totientCoprime, message):
        codedMessage = ""
        for x in message:
            currentModule = (ord(x)-96) % n
            resultOfExpoModN = 1
            for y in range(totientCoprime):
                resultOfExpoModN = resultOfExpoModN*currentModule
            codedMessage += str(resultOfExpoModN%n) + "/"
        return codedMessage[:-1]

    def decodeMessage(self, n, totientCoprimeInverseModTotient, codedMesage):
        decodedMessage = ""
        x = codedMesage.split("/")
        for y in x:
            resultOfExpoModN = 1
            for z in range(totientCoprimeInverseModTotient):
                resultOfExpoModN = resultOfExpoModN * int(y)
            decodedMessage += str(chr((resultOfExpoModN % n)+96))
        return decodedMessage

if __name__ == "__main__":          
    gg = rsa()
    print(gg.codificateMessage(33,7,"holaz"))
    print(gg.decodeMessage(33,3,gg.codificateMessage(33,7,"holaz")))
    print(gg.findInverse(7,20))