#nome del file : pagellaClientMulti.py
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    studenti=["Colombo","D'Alba","Di Lorenzo","Falcone","Ghidoli"]
    materie=["Matematica","Italiano","Inglese","Storia","Geografia"]
    #   di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    numero = random.randint(0,4)
    studente=studenti[numero]
    #   di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    numero = random.randint(0,3)
    materia=materie[numero]
    #   di un voto (valori ammessi 1 ..10)
    voto=random.randint(1,10)
    #   delle assenze (valori ammessi 1..5) 
    assenze=random.randint(1,5)
    #2. comporre il messaggio, inviarlo come json
    #   esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    messaggio = {
        'studente': studente,
        'materia': materia,
        'voto': voto,
        'assenze': assenze
    }
    messaggio=json.dumps(messaggio)
    print("Invio richiesta:", messaggio)
    s.sendall(messaggio.encode("UTF-8"))

    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}
    data=s.recv(1024)
    data=json.loads(data)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        #4 stampare la valutazione ricevuta esempio: La valutazione di Studente4 in italiano è Gravemente insufficiente
        print("La valutazione di", data['studente'], "in", data['materia'], "è", data['valutazione'])
    s.close()

#Versione 2 
def genera_richieste2(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #....
    #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)
    studenti=["Colombo","D'Alba","Di Lorenzo","Falcone","Ghidoli"]
    numero = random.randint(0,4)
    studente=studenti[numero]
    #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia
    #   generazione di un voto (valori ammessi 1 ..10)
    #   e delle assenze (valori ammessi 1..5)

    # pagella={"Giuseppe Gullo":[("matematica",9,0),("Italiano",7,3),("inglese",7.5,4),("Storia",7.5,4),("GEografia",5,7)],
    #      "Antonio Barbera":[("matematica",8,1),("Italiano",6,1),("inglese",9.5,0),("Storia",8,2),("GEografia",8,1)],
    #      "Nicola Spina":[("matematica",7.5,2),("Italiano",6,2),("inglese",4,3),("Storia",8.5,2),("GEografia",8,2)]}

    studenteEPagella={"studente": studente, "pagella":[]}
    materie=["Matematica","Italiano","Inglese","Storia","Geografia"]
    for materia in materie:
        voto=random.randint(1,10)
        assenze=random.randint(1,5)
        studenteEPagella["pagella"].append((materia, voto, assenze))
    
    #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
    #2. comporre il messaggio, inviarlo come json
    messaggio = {
        'studente': studente,
        'pagella': studenteEPagella["pagella"]
    }
    messaggio=json.dumps(messaggio)
    print("Invio richiesta:", messaggio)
    s.sendall(messaggio.encode("UTF-8"))
    #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}
    data=s.recv(1024)
    data=json.loads(data)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print("Lo studente", data["studente"], "ha una media di", data["mediaVoti"], "e un totale di assenze di", data["sommaAssenze"])

#Versione 3
def genera_richieste3(num,address,port):
    #....
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
    tabellone = {}
    studenti=["Colombo","D'Alba","Di Lorenzo","Falcone","Ghidoli"]
    materie=["Matematica","Italiano","Inglese","Storia","Geografia"]

    for studente in studenti:
        votiEAssenze = []
        for materia in materie:
            voto = random.randint(1,10)
            assenze = random.randint(1,5)
            votiEAssenze.append((materia, voto, assenze))
        tabellone[studente] = votiEAssenze
    #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
    #   generazione di un voto (valori ammessi 1 ..10)
    #   e delle assenze (valori ammessi 1..5) 
    #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
    #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
    #                        .....}
    messaggio = {
        'tabellone': tabellone
    }
    messaggio=json.dumps(messaggio)
    print("Invio richiesta:", messaggio)
    s.sendall(messaggio.encode("UTF-8"))
    #2. comporre il messaggio, inviarlo come json
    #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3
    data=s.recv(1024)
    data=json.loads(data)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        for e in data:
            print("Lo studente ", {e['studente']}, "ha una media di ", {e['media']}, "e un totale di assenze di ", {e['assenze']})

if __name__ == '__main__':
    start_time=time.time()
    # PUNTO A) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)
    # alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    for num in range(NUM_WORKERS):
        genera_richieste3(num, SERVER_ADDRESS, SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
    print("FINE PUNTO 1")
    start_time=time.time()
    # PUNTO B) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)  
    # tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i thread e attenderne la fine
    threads=[]
    for num in range(NUM_WORKERS): #NUM_WORKERS volte
        thread = threading.Thread(target=genera_richieste3, args=(num, SERVER_ADDRESS, SERVER_PORT)) #creo il thread che svolge genera_richieste, con come argomenti args
        # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)
    print("FINE PUNTO 2")

    start_time=time.time()
    processes=[]
    # PUNTO C) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3) 
    # tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    for num in range(NUM_WORKERS): #NUM_WORKERS volte
        process = multiprocessing.Process(target=genera_richieste3, args=(num, SERVER_ADDRESS, SERVER_PORT)) #creo il thread che svolge genera_richieste, con come argomenti args
        # ad ogni iterazione appendo il thread creato alla lista threads
        processes.append(process)
    # 8 avvio tutti i processi
    for process in processes:
        process.start()
    # 9 aspetto la fine di tutti i processi 
    for process in processes:
        process.join()
    # avviare tutti i processi e attenderne la fine
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)