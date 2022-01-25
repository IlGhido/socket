import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        stringa=input('Inserire la stringa, "KO" per uscire: ')
        messaggio={
            'stringa' : stringa
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto in una stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        if stringa=="KO":
            print(data.decode())
            break
        else:
            print("Stringa modificata: ", data.decode())