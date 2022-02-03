import socket
import json

HOST="127.0.0.1"
PORT=65432

def invia_comandi(sock_service):
    while True:
        primoNumero=input("Inserisci il primo numero exit() per uscire: ")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("Inserisci l'operazione (+,-,*,/,%): ")
        secondoNumero=float(input("Inserisci il secondo numero: "))
        messaggio={
            'primoNumero':primoNumero, 
            'operazione':operazione, 
            'secondoNumero':secondoNumero
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto in una stringa
        sock_service.sendall(messaggio.encode("UTF-8"))
        data=sock_service.recv(1024)
        print("Risultato: ", data.decode())

def connessione_server(address,port):
    sock_service = socket.socket()
    sock_service.connect((address, port))
    print("Connesso a " + str((address, port)))
    invia_comandi(sock_service)

if __name__=='__main__':
    connessione_server(HOST,PORT)