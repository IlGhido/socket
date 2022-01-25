import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    contatore=1
    s.bind((HOST,PORT))
    s.listen()
    print("[*] In ascolto su %s:%d"%(HOST,PORT))
    clientsocket, address = s.accept()
    with clientsocket as cs:
        print("Connessione da ", address)
        while True:
            data=cs.recv(1024)
            if not data:
                break
            data=data.decode()
            data=json.loads(data)
            stringa=data['stringa']
            if stringa != "KO":
                ris="Messaggio numero " + str(contatore) + ": " + stringa
                contatore += 1
            else:
                ris='Ricevuto "KO" dal server, chiudo la connessione con il client.'
            cs.sendall(ris.encode("UTF-8"))