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
        self.e = self.find_e(self.totient)
        self.d = RSA.find_inverse(self.e, self.totient)
        self.public_key = (self.n, self.e)
        self.private_key = self.d
    
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
        for x in range(2, totient):
            if (e*x)%totient == 1:
                return x
        return 0

    def fast_exponentiation(base, exponent):
        '''
        Exponentiation-by-squaring algorithm.
        '''
        binary_exponent = f"{exponent:b}"
        result = base
        for binary_digit in binary_exponent[1:]:
            result = result * result
            if(int(binary_digit)==1):
                result = result * base
        return result

    #using fast_exponentiation
    def codificate_message(self, n, e, message):
        coded_message = ""
        for x in message:
            x_ascii = ord(x)%n
            encoded_ascii = RSA.fast_exponentiation(x_ascii, e)
            coded_message += str(encoded_ascii%n) + "/"
        return coded_message[:-1]

    def decode_message(self, coded_message):
        decoded_message = "" 
        coded_message = coded_message.split("/")
        for y in coded_message:
            result_modular_exp = RSA.fast_exponentiation(int(y), self.d)
            decoded_message += str(chr(result_modular_exp%self.n))
        return decoded_message

if __name__ == "__main__":          
    
    #191 193 197 199 211 223 227 229
    #233 239 241 251 257 263 269 271 277 281
    #283 293 307
    #Test
    Alice = RSA(191, 193)
    Bob = RSA(241,239)
    Chuck = RSA(211, 223)
    print("Bob n {}, e {}, totient {}, d {}".format(Bob.n, Bob.e, Bob.totient, Bob.d))
    print("Alice n {}, e {}, totient {}, d {}".format(Alice.n, Alice.e, Alice.totient, Alice.d))
    print("Chuck n {}, e {} , totient {}, d {}".format(Chuck.n, Chuck.e, Chuck.totient, Chuck.d))

    #Alice sends a message to Bob
    #somehow send Bob's pk to Alice at the start, use Bob's pk to encrypt

    alice_message = Alice.codificate_message(Bob.n, Bob.e, "And yet it works")
    print("encrypted msg by alice ", alice_message)
    # Bob uses d to decrypt
    bob_decrypt = Bob.decode_message(alice_message)
    print("Bob decrypts Alice msg: ", bob_decrypt)

    
    bob_message = Bob.codificate_message(Alice.n, Alice.e, "hopefully")
    print("encrypted msg by bob ", bob_message)
    alice_decrypt = Alice.decode_message(bob_message)
    print("Alice decrypts Bob's msg", alice_decrypt)

    
    #Now Chuck tries to read their messages using his private key
    chuck_decrypts_alice = Chuck.decode_message(alice_message)
    chuck_decrypts_bob = Chuck.decode_message(bob_message)

    print("Chuck starts")
    print("Chuck tries to decrypt alice's msg", chuck_decrypts_alice)
    print("Chuck tries to decrypt bob's msg", chuck_decrypts_bob)