import socket
import json

HOST="127.0.0.1"
PORT=65432

def invia_comandi(sock_service):
    while True: #serie di operazioni che permette all'utente di inserire i numeri e l'operazione da effettuare con la calcolatrice, poi invia il messaggio al server. Quando gli torna il messaggio lo decodifica e lo restituisce in output.
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

def connessione_server(address,port): #funzione che raggruppa le istruzioni per connettersi al server e poi fa l'output in caso di connessione riuscita
    sock_service = socket.socket()
    sock_service.connect((address, port))
    print("Connesso a " + str((address, port)))
    invia_comandi(sock_service)

if __name__=='__main__':
    connessione_server(HOST,PORT)