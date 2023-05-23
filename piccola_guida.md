# Piccola guida di robotica
> Samuele Facenda

Una piccolo (per quello che si potrebbe dire) documento con quello che io (Samuele Facenda) ho imparato e ho da dire sulla robotica all'ITT Buonarroti. 
Espone un paio di aspetti e soprattutto include link utili per capire come fare alcune cose, che vanno dal riconoscimento dei caratteri alla mappatura del labirinto o all'allineamento del robot.

Non sono un elettronico né un automatico, ma un informatico. Non farò riferimento al funzionamento dei sensori o dei motori, parlerò solo dell'aspetto informatico (inteso come codice e gesitone).

## 1 - Gestione del robot

Il robot ha motissimi componenti diversi, essi devono essere coordinati nelle loro azioni. Ci sono i sensori e i motori, collegati con il robò. 
Il modo più semplice per interfacciarsi con i componenti è usando una scheda arduino, ci sono un sacco di librerie comode e codici boilerplate in internet.

### 1.1 Arduino

Arduino è praticamente c++, cambia però la struttura del progetto, che viene molto semplificata.

#### 1.1.1 Struttura di un progetto arduino

La struttura **deve** essere così composta:

directory root (si chiama come lo sketch principale):
- sketch principale (file.ino)
- codice aggiuntivo.h
- codice aggiuntivo.cpp
- codice aggiuntivo2.h
- codice aggiuntivo2.cpp

In c++ si deve definire in un file le funzioni e le classi e queste vanno implementate in un altro file, rispettivamente i file .h (header) e .cpp. Arduino in automatico riconosce questa divisione e include le funzioni, classi e costanti così definite nello sketch principale (file .ino con funzioni setup e loop)

#### 1.1.2 Comunicazione seriale

Per comunicare via seriale (un canale con input e output divisi e comodo da usare) con altri dispositivi da arduino si può usare la classe Serial che con i metodi println ad esempio invia una stringa con il carattere di a capo alla fine sulla porta principale, quella usb (quindi il computer di solito). 

Questa è comoda per il debug, mentre per le comunicazioni con altri dispositivi si possono usare le porte seriali ausiliari. Queste sono coppie di pin, segnati come RX e TX (transmit e recive), la prima è utilizzabile come quella principale con la classe Serial1 (e.g. Serial1.println). Dall'altro capo ci deve essere collegato un dispositivo (arduino, raspberry o altra cosa che sia) che comunica in seriale.

Se questi pin sono occupati o si necessità un setup diverso, qualunque pin può essere usato come rx/tx, con la libreria arduino [Software Serial](https://docs.arduino.cc/learn/built-in-libraries/software-serial). Al link si trovano le informazioni necessarie

### 1.2 Raspberry

I raspberry pi sono single board computer economici (:no_mouth:) con dei pin gpio ([pinout](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHLwG7rR3G1PxzagBjpEEFUbROI1XL4yMHP7DI5ghN&s)). 
[Qui](https://projects.raspberrypi.org/en/projects/physical-computing) ci sono delle informazioni sul loro utilizzo con python (se non si è pratici con python è comodo impararlo, è semplice, [qui](https://www.programiz.com/python-programming) un corso base).

#### 1.2.1 Setup

Sul raspberry va installato linux (architettura ARM), raspbian è fatto apposta, comunque [qui](https://www.raspberrypi.com/documentation/computers/getting-started.html) c'è la guida introduttiva ufficiale. Io mi sono sempre connesso con ssh o vnc, quando usi [raspberry pi image](https://www.raspberrypi.com/software/) per creare la schedina col sistema operativo puoi assegnargli una wifi a cui connettersi e un hostname per riconoscerlo. 

#### 1.2.2 Comunicazione seriale

Per comunicare in seriale con qualunque altro dispositivo con qualunque porta (le usb o i pin rx tx del raspberry) [pyserial](https://pyserial.readthedocs.io/en/latest/) è perfetta, basta cercare qualche esempio per capire come funziona.

### 1.3 Gestione dei processi

Sul raspberry soprattutto è importante coordinare tutti i moduli perchè siano coesi (e.g. lettura sensori, esplorazione, movimenti). 
Con python semplice o qualunque altro linguaggio si possono usare in thread ([libreria threading ufficiale](https://docs.python.org/3/library/threading.html)), in python con le classi Thread, Lock (un mutex), Semaphore e Event(un flag booleano sincronizzato).

### 1.4 ROS
[Robot OS](https://www.ros.org/) è un framework molto comodo per gestire tutti i processo e componenti di un pc con linux (raspberry), ti permette di definirli come nodi indipendenti e di lasciarlo ad occuparsi della loro gestione e comunicazione. 
[Qui](https://docs.ros.org/en/humble/index.html) c'è la documentazione dell'LTS al 2023, comsiglio di leggerla prima di cominciare ad usarlo, soprattutto i tutorial da beginner.

## 2 - Riconoscimento delle vittime



## 3 - Mappatura e esplorazione

## 4 - Movimenti

## 5 - Note finali
