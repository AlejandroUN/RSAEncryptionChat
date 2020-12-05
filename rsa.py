# -----------------------------------------------------------
# 
# 
# (C) 2020
# -----------------------------------------------------------

import random

class RSA:


    def __init__(self, p, q):

        #soon get random p and q using Miller-Rabin
        #devolverlo esto a user de nuevo
        #primes = [i for i in range(1000,2000) if RSA.isPrime(i)]
        #some random primes 14741 17159 1866367 1105141
        self.p = p
        self.q = q
        self.n = self.p*self.q
        self.totient = RSA.find_totient(self.p, self.q)
        self.e = RSA.find_e(self.totient)
        self.d = RSA.find_inverse(self.e, self.totient)
    
    def find_totient(p, q):
        return ((p-1)*(q-1))

    #findTotientCoprime not working
    def find_e(totient):
        posible_e = [3,5,17,257, 65537]
        return random.choice(posible_e)
        '''
        for x in range(2, totient):

            if RSA.gcd(x,totient) == 1:
                return x
        return 0
        '''

    @staticmethod
    def isPrime(n): 
        i = 2
        while(i * i <= n): 
            if (n % i == 0): 
                return False; 
            i = i + 1; 
        return True

    @staticmethod
    def gcd(a, b):
        if a%b == 0:
            return b
        else:
            return RSA.gcd(b, a%b)

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = RSA.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def find_inverse(a, m):
        g, x, y = RSA.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def find_inverse2(e, totient):
        for x in range(totient-1):
            if ((e*(x+1))%totient) == 1:
                return (x+1)
        return 0


    def fast_exponentiation(base, exponent, modulus):
        '''
        Exponentiation-by-squaring algorithm.
        '''
        binary_exponent = f"{exponent:b}"
        result = base

        for binary_digit in range(len(binary_exponent)-1, 0):
            result = (result*result) % modulus
            if(binary_digit==1):
                result = (result * base) % modulus
        return result
    
    #using fast_exponentiation
    def codificate_message(self, message):
        coded_message = ""
        for x in message:
            x_ascii = ord(x)
            encoded_ascii = RSA.fast_exponentiation(x_ascii, self.e, self.n)
            coded_message += str(encoded_ascii) + "/"
        return coded_message[:-1]


    def decode_message(self, coded_message):
        decoded_message = "" 
        coded_message = coded_message.split("/")
        for y in coded_message:
            result_modular_exp = RSA.fast_exponentiation(int(y), self.d, self.n)
            decoded_message += str(chr(result_modular_exp))
        return decoded_message

    '''
    def codificate_message(self, n, e, message):
        coded_message = ""
        for x in message:
            current_module = (ord(x)-96) % n
            result_modular_exp = 1
            for y in range(e):
                result_modular_exp = result_modular_exp*current_module
            coded_message += str(result_modular_exp%n) + "/"
        return coded_message[:-1]

    def decode_message(self, n, d, coded_message):
        decoded_message = "" 
        x = coded_message.split("/")
        for y in x:
            result_modular_exp = 1
            for z in range(d):
                result_modular_exp = result_modular_exp * int(y)
            decoded_message += str(chr((result_modular_exp % n)+96))
        return decoded_message
    '''
if __name__ == "__main__":          
    
    gg = RSA(283,863)
    
    una_cadena2 = gg.codificate_message("I'm funny how, I mean funny like I'm a clown?")
    print(gg.decode_message(una_cadena2))
    print("p: ",gg.p)
    print("g: ",gg.q)
    print("n: ",gg.n)
    print("e: ",gg.e)
    print("totient: ", gg.totient)
    print("d: ",gg.d)
    print(RSA.gcd(12,8))
    print(RSA.gcd(8,12))