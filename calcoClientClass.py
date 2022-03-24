import socket
import json
import random
SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=22225

class Client():
    def invia_comandi(self,sock_service):
        primoNumero=random.randint(1,10)
        secondoNumero=random.randint(1,10)
        operazioni=["+","-","*","/","%"]
        operazione=random.choice(operazioni)
        messaggio={
            'primoNumero':primoNumero, 
            'operazione':operazione, 
            'secondoNumero':secondoNumero
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto in una stringa
        sock_service.sendall(messaggio.encode("UTF-8"))
        data=sock_service.recv(1024)
        print("Primo numero:", primoNumero)
        print("operazione:", operazione)
        print("Secondo numero:", secondoNumero)
        print("Risultato: ", data.decode())

    def connessione_server(self,address,port): #funzione che raggruppa le istruzioni per connettersi al server e poi fa l'output in caso di connessione riuscita
        sock_service = socket.socket()
        sock_service.connect((address, port))
        print("Connesso a " + str((address, port)))
        return sock_service

c1=Client()
sock_serv=c1.connessione_server(SERVER_ADDRESS,SERVER_PORT)
c1.invia_comandi(sock_serv)