#SERWER
import ssl
import numpy as np
import socket, threading
import time

plansza = np.array([[0,0,0] for i in range(3)])
aktualny_gracz = 1

ostatni_ruch = -1
def set_ostatni_ruch(number):
    global ostatni_ruch
    ostatni_ruch = number

def reset_planszy():
    global plansza
    plansza = np.array([[0,0,0] for i in range(3)])
def aktualny_gracz_f():
    return aktualny_gracz
    
def get_plansza():
    return plansza.copy()
def set_plansza(new_plansza):
    global plansza
    plansza = new_plansza
    
def wykonaj_ruch(x,y,gracz):
    plansza = get_plansza()
    if plansza[x][y] != 0:
        return "pole zajete"
    else:
        plansza[x][y] = gracz
        set_plansza(plansza)
    return "udalo sie"
def zmien_gracza():
    global aktualny_gracz 
    aktualny_gracz= (-1)*aktualny_gracz
    
def tlumacz_na_x_y(ruch):
    if ruch == 1:
        return 0,0
    if ruch == 2:
        return 0,1
    if ruch == 3:
        return 0,2
    if ruch == 4:
        return 1,0
    if ruch == 5:
        return 1,1
    if ruch == 6:
        return 1,2
    if ruch == 7:
        return 2,0
    if ruch == 8:
        return 2,1
    if ruch == 9:
        return 2,2
    else:
        return None
    
    
def czy_koniec():
    for i in range(3):
        if plansza[i][0] == plansza[i][1] and  plansza[i][2] == plansza[i][1] and  plansza[i][2] !=0:
            return plansza[i][0]
    for i in range(3):
        if plansza[0][i] == plansza[1][i] and  plansza[2][i] == plansza[1][i] and plansza[2][i] !=0:
            return plansza[0][i]
    if plansza[0][0] == plansza[1][1] and plansza[1][1] == plansza[2][2] and plansza[1][1] != 0:
        return plansza[0][0]
    if plansza[0][2] == plansza[1][1] and plansza[1][1] == plansza[2][0] and plansza[1][1] != 0:
        return plansza[0][0]
    czy_koniec_1 = True
    for i in range(3):
        for j in range(3):
            print(plansza[i][j])
            if plansza[i][j] == 0:
                czy_koniec_1 = False
    if czy_koniec_1:
        return 0
    else:
        return 2

def podaj_wyglad_planszy():
    wyglad = ""
    for i in range(3):
        for j in range(3):
            if plansza[i][j] == 0:
                wyglad += " "
            elif plansza[i][j] == 1:
                wyglad += "O"
            else:
                wyglad += "X"
    return wyglad



wykonaj_ruch(2,1,1)


# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain(r'C:\Users\patryk.krawczak\Downloads\server.crt', r'C:\Users\patryk.krawczak\Downloads\server.key')
def create_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile= r'C:\Users\patryk.krawczak\Downloads\server.crt', keyfile= r'C:\Users\patryk.krawczak\Downloads\server.key')
    context.load_verify_locations(cafile=r'C:\Users\patryk.krawczak\Downloads\client.crt')
        
    return context

context = create_context()



class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,numer_gracza):
        print("startuje")
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.numer_gracza = numer_gracza
        
    def run(self):
        msg = ''
        self.csocket.sendall(b"i am ready")
        while True:
#             if aktualny_gracz_f() == self.numer_gracza:
            data = self.csocket.recv(1048)
            print("got it!"+str(self.numer_gracza))
            msg = data.decode()
            if msg == "koniec":
                global licznik_graczy
                licznik_graczy -= 1
                return
            if msg == "START":
                self.csocket.send(b"ok")
                i = 0
                
                while True:
                    if aktualny_gracz_f() != self.numer_gracza:
                         
                        self.csocket.send(b"musisz poczekac")
                        
                        data = self.csocket.recv(10)
                        if data == b"ok":
                            while aktualny_gracz_f() != self.numer_gracza:
                                time.sleep(1)
                                print(aktualny_gracz_f(),self.numer_gracza)
                    else:
                        wiadomosc = podaj_wyglad_planszy()
                        print("plansza wygląda tak:",wiadomosc)
                        wiadomosc = "podaj ruch"+wiadomosc
                        self.csocket.send(wiadomosc.encode()) 
                        data = self.csocket.recv(10)
                        data = data.decode()
                        data = int(data)
                        if tlumacz_na_x_y(data) is not None:
                            x,y = tlumacz_na_x_y(data)
                            wynik = wykonaj_ruch(x,y,self.numer_gracza)
                            if wynik == "udalo sie":
                                zmien_gracza()
                                set_ostatni_ruch(data)
                                if czy_koniec() == 2:
                                    self.csocket.send("ok2".encode())
                                    while aktualny_gracz_f() != self.numer_gracza:
                                        pass
                                    ruch_przeciwnika = str(ostatni_ruch)
                                    self.csocket.send(ruch_przeciwnika.encode())
                                else:

                                    wynik = "ok"+str(czy_koniec())
                                    self.csocket.send(wynik.encode())
                                    break
                            else:
                                self.csocket.send(b"nieprawidlowy ruch")
                        else:
                            self.csocket.send(b"nieprawidlowy ruch")
                        
                



LOCALHOST = "127.0.0.1"
PORT = 8082

licznik_graczy = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', PORT))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        
        print("Server started")
        while True:
            if licznik_graczy < 2:
                clientsock, clientAddress = ssock.accept()
                newthread = ClientThread(clientAddress, clientsock,aktualny_gracz_f())
                newthread.start()
                zmien_gracza()
                licznik_graczy += 1
            
## CLIENT
