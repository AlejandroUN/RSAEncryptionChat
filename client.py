import socket
import select
import errno
import re
import random
import sys
from rsa import RSA


HEADER_LENGTH = 100

IP = ""127.0.0.1""
PORT = 5555
FORMAT = 'utf-8'

if(len(sys.argv) < 6):
    print("{}-{}".format(sys.argv[1], sys.argv[2]))
    rsa = RSA(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("Ejecute los primos en la forma python client.py primo1 primo2")
    exit()

user_n, user_e = rsa.public_key
user_n = user_n
user_e = user_e

public_key = "{}-{}".format(user_n, user_e)

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to server
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = public_key.encode(FORMAT)

username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)

client_socket.send(username_header + username)

other_user_pk = None
other_user_n = None
other_user_e = None

while True:

    message = input(f'{public_key} > ')

    if message:

        # Encode message to bytes
        if(other_user_pk != None):
            print("Enviando mensaje a usuario con pk", message, other_user_n, other_user_e)
            message = rsa.codificate_message(other_user_n, other_user_e, message)
            message = message.encode(FORMAT)
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)
            client_socket.send(message_header + message)
        else: 
            print("Esperando otro usuario. No se encodificara ningun mensaje")
            message = '0'.encode(FORMAT)
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)
            client_socket.send(message_header + message)

    try:

        # We need to get the other person's public key. We do it in form of a username

        while True:

            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, close connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode(FORMAT).strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode(FORMAT)

            # For now the other user's pk is his username. So take it and encrypt messages with them
            
            other_user_pk = re.split("-", username)
            other_user_n = int(other_user_pk[0])
            other_user_e = int(other_user_pk[1])

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode(FORMAT).strip())

            message = client_socket.recv(message_length).decode(FORMAT)
            mensaje = rsa.decode_message(message)

            print(f'{username} > {mensaje}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()