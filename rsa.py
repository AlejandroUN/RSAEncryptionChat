# -----------------------------------------------------------
# 
# 
# (C) 2020
# -----------------------------------------------------------

import random

class RSA:


    def __init__(self, p, q):

        #soon get random p and q using Miller-Rabi
        self.p = p
        self.q = q
        self.n = self.p*self.q
        self.totient = RSA.find_totient(self.p, self.q)
        self.e = self.find_e(self.totient)
        self.d = RSA.find_inverse(self.e, self.totient)
        self.public_key = (self.n, self.e)
        self.private_key = self.d

        self.cp = RSA.find_inverse(self.q, self.p)
        self.cq = RSA.find_inverse(self.p, self.q)
    
    def find_totient(p, q):
        return ((p-1)*(q-1))

    def find_e(self, totient):
        
        for integer in range(3, self.totient):
            if(RSA.gcd(self.totient, integer) == 1):
                return integer


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

    def find_inverse(e, totient):
        m0 = totient
        y = 0
        x = 1
        if (totient == 1):
            return 0
        while (e > 1):
            q = e // totient
            t = totient
            totient = e % totient
            e = t
            t = y
            y = x - q * y
            x = t
        if (x < 0):
            x = x + m0
        return x

def fast_exponentiation(base, exponent, modulus):
        '''
        Exponentiation-by-squaring algorithm.
        '''
        binary_exponent = f"{exponent:b}"
        result = base
        for binary_digit in binary_exponent[1:]:
            result = (result * result) % modulus 
            if(int(binary_digit)==1):
                result = (result * base) % modulus  
        return result

    #using fast_exponentiation
    def codificate_message(self, n, e, message):
        coded_message = ""
        for x in message:
            x_ascii = ord(x)
            encoded_ascii = RSA.fast_exponentiation(x_ascii, e, n)
            coded_message += str(encoded_ascii) + "/"
        return coded_message[:-1]

    def decode_message(self, coded_message, crt = True, modular=False):
        decoded_message = "" 
        coded_message = coded_message.split("/")
        for y in coded_message:
            if crt: result_modular_exp = self.crt_domain_reduction(int(y))
            if modular: result_modular_exp = RSA.fast_exponentiation(int(y), self.d, self.n)
            decoded_message += str(chr(result_modular_exp))
        return decoded_message

    def crt_domain_reduction(self, x):
        x_p = x % self.p
        x_q = x % self.q

        d_p = self.d % (self.p-1)
        d_q = self.d % (self.q-1)

        y_p = RSA.fast_exponentiation(x_p, d_p, self.p)
        y_q = RSA.fast_exponentiation(x_q, d_q, self.q)

        c_p = self.cp
        c_q = self.cq

        return ((self.q*c_p)*y_p + (self.p*c_q)*y_q)% self.n

if __name__ == "__main__":          

    Alice = RSA(191, 193)
    Bob = RSA(241,239)
    Chuck = RSA(211, 223)

    print("Bob n {}, e {}, totient {}, d {} cp {} cq {}".format(Bob.n, Bob.e, Bob.totient, Bob.d, Bob.cp, Bob.cq))
    print("Alice n {}, e {}, totient {}, d {} cp {} cq {}".format(Alice.n, Alice.e, Alice.totient, Alice.d, Alice.cp, Alice.cq))
    print("Chuck n {}, e {} , totient {}, d {} cp {} cq {}".format(Chuck.n, Chuck.e, Chuck.totient, Chuck.d, Chuck.cp, Chuck.cq))

    #Alice sends a message to Bob
    #somehow send Bob's pk to Alice at the start, use Bob's pk to encrypt

    alice_message = Alice.codificate_message(Bob.n, Bob.e, "you now quasimodo predicted all of this")
    print("Encrypted msg by alice ", alice_message)
    # Bob uses d to decrypt
    bob_decrypt = Bob.decode_message(alice_message)
    print("Bob decrypts Alice msg: ", bob_decrypt)

    
    bob_message = Bob.codificate_message(Alice.n, Alice.e, "who did what")
    print("encrypted msg by bob ", bob_message)
    alice_decrypt = Alice.decode_message(bob_message)
    print("Alice decrypts Bob's msg", alice_decrypt)

    #Now Chuck tries to read their messages using his private key
    chuck_decrypts_alice = Chuck.decode_message(alice_message)
    chuck_decrypts_bob = Chuck.decode_message(bob_message)

    print("Chuck starts")
    print("Chuck tries to decrypt alice's msg", chuck_decrypts_alice)
    print("Chuck tries to decrypt bob's msg", chuck_decrypts_bob)

    