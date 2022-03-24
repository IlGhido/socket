from ctypes import addressof
import socket
from threading import Thread
import json

SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=22225

class Server():
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def ricevi_comandi(self, sock_service, addr_client): #funzione che permette al server di ricevere i comandi inviati dal client
        print("avviato")
        while True: #serie di operazioni, il server riceve i dati dal client tramite il sock, li elabora eseguendo l'operazione e restituisce il risultato, infine chiude il sock
            data=sock_service.recv(1024)
            if not data:
                break
            data=data.decode()
            data=json.loads(data)
            primoNumero=data['primoNumero']
            operazione=data['operazione']
            secondoNumero=data['secondoNumero']
            ris=""
            if operazione=="+":
                ris=primoNumero+secondoNumero
            elif operazione=="-":
                ris=primoNumero-secondoNumero
            elif operazione=="*":
                ris=primoNumero*secondoNumero
            elif operazione=="/":
                if secondoNumero==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="Operazione non riconosciuta"
            ris=str(ris)
            sock_service.sendall(ris.encode("UTF-8"))
        sock_service.close()

    def ricevi_connessioni(self, sock_listen): #funzione che permette di ricevere la connessione dai client, e poi crea il thread per mandare in esecuzione le richieste
        while True:
            sock_service, addr_client = sock_listen.accept()
            print("\nConnessione ricevuta da " + str(addr_client))
            print("\nCreo un thread per servire le richieste")
            try: #caso in cui il thread viene creato con successo
                Thread(target=self.ricevi_comandi, args=(sock_service,addr_client)).start()
            except: #caso in cui il thread non viene avviato con successo, si chiude la connessione con il client
                print("Il thread non si avvia")
                sock_listen.close()

    def avvia_server(self): #funzione che permette di avviare un server, quindi si prepara a ricevere le connessioni dei client
        sock_listen=socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_listen.bind((self.address, self.port))
        sock_listen.listen(5)
        print("Server in ascolto su %s." % str((self.address, self.port)))
        return sock_listen

s1 = Server(SERVER_ADDRESS, SERVER_PORT)
sock_list=s1.avvia_server()
s1.ricevi_connessioni(sock_list)