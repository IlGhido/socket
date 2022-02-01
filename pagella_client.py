import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        stringa=input('Comandi disponibili:\n#list : per vedere i voti inseriti \n#set /nomestudente : per inserire uno studente \n#put /nomestudente/materia/voto/ore : per aggiungere i voti della materia allo studente \n#get /nomestudente : per richiedere i voti di uno studente \n#exit : per chiudere solo il client\n')
        if (stringa.find('#exit') != -1):
            print("\nChiusura client")
            break

        messaggio={
            'stringa' : stringa
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto in una stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        if (stringa.find('#list') != -1):
            deserialized_voti = json.loads(data)
        # elif (stringa.find('#set') != -1 or stringa.find('#get') != -1 or stringa.find('#put') != -1):
        else:
            deserialized_voti = data.decode()
        print("\n"+deserialized_voti+"\n")
