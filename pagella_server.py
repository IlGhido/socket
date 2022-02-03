import socket
import json

HOST="127.0.0.1"
PORT=65432
voti = {'Giuseppe Gullo':[("Matematica",9,0),("Italiano",7,3),("Inglese",7.5,4),("Storia",7.5,4),("Geografia",5,7)],
           'Antonio Barbera':[("Matematica",8,1),("Italiano",6,1),("Inglese",9.5,0),("Storia",8,2),("Geografia",8,1)],
           'Nicola Spina':[("Matematica",7.5,2),("Italiano",6,2),("Inglese",4,3),("Storia",8.5,2),("Geografia",8,2)]}

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

            if (stringa.find('#lis') != -1):
                serialized_voti = json.dumps(voti)
                cs.sendall(serialized_voti.encode())

            elif (stringa.find('#set') != -1):
                serieStringhe=stringa.split('/')
                nome = serieStringhe[1]
                if(nome in voti):
                    cs.sendall("studente già presente".encode())
                else:
                    voti[nome] = []
                    cs.sendall("studente inserito".encode())
            
            elif (stringa.find('#put') != -1):
                presente = False
                # Il comando put deve verificare che lo studente esista e che la materia non esista
                serieStringhe=stringa.split('/')
                nome = serieStringhe[1]
                materia = serieStringhe[2]
                if(nome in voti):
                    for studente, materiaPagella in voti.items():
                        if(studente == nome):
                            for i in materiaPagella:
                                print(materiaPagella)
                                if(materia == i[0]):
                                    print(i[0])
                                    presente=True
                    if(presente == False):
                        voto = int(serieStringhe[3])
                        ore = int(serieStringhe[4])
                        nuovaMateria = [materia, voto, ore]
                        voti[nome].append(nuovaMateria)
                        cs.sendall("voto inserito".encode())
                    else:
                        cs.sendall("materia già presente".encode())
                else:
                    cs.sendall("studente non presente".encode())


            elif (stringa.find('#get') != -1):
                stringaVoti = ""
                serieStringhe=stringa.split('/')
                nome = serieStringhe[1]
                if(nome in voti):
                    serialized_voti = json.dumps(voti[nome])
                    cs.sendall(serialized_voti.encode())
                else:
                    listaStringa = ["studente non presente"]
                    serialized_voti = json.dumps(listaStringa)
                    cs.sendall(serialized_voti.encode())
            else:
                cs.sendall("Comando non trovato".encode())