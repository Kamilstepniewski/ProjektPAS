# SERWER
import ssl
import uuid

import numpy as np
import socket, threading
import time


def opakuj(To, From, Information_about_client_sesion_id, Message_id, Content_length, Message):
    return f"To:{To}\r\nFrom:{From}\r\nInformation_about_client_sesion_id:{Information_about_client_sesion_id:39}\r\nMessage_id:{Message_id:03}\r\nContent_length:{Content_length:03}\r\nMessage:{Message}\r\n\r\n"


def odpakuj(msg):
    for i in msg:
        print([i])
    to = msg[3:6]
    From = msg[13:16]
    Info_id = msg[53:92]
    print("Odpakuj: ", Info_id)
    Message_id = msg[105:108]
    Content_length = msg[125:128]
    Content_length = int(Content_length)
    message = msg[138:138 + Content_length]
    return to, From, Info_id, Message_id, Content_length, message


def read_message(message):
    # Tutaj można odbierać wiadomość dopóki b'\r\n\r\n' not in data
    # data = b''
    # while b'\r\n\r\n' not in data:
    #    data += client.recv(1)
    print(message)
    To = message[3:9]
    From = message[16:16 + 3]
    Information_about_client_sesion_id = message[56:56 + 38]

    #     print(message.find("Content_length:") + len("Content-length:"))
    Content_length = int(message[92 + len("Content_length:"):93 + 2 + len("Content_length:")])
    Message_id = message[106:106 + 3]
    # len = 8+Content_length
    Message = message[140:140 + Content_length]
    print("-------")
    print(
        f"To:{To}\r\nFrom:{From}\r\nInformation_about_client_sesion_id:{Information_about_client_sesion_id}\r\nMessage_id:{Message_id}\r\nContent_length:{Content_length}\r\nMessage:{Message}")
    return To, From, Information_about_client_sesion_id, Message_id, Content_length, Message


plansza = np.array([[0, 0, 0] for i in range(3)])

aktualny_gracz = 1

ostatni_ruch = -1


def set_ostatni_ruch(number):
    global ostatni_ruch
    ostatni_ruch = number


def reset_planszy():
    global plansza
    plansza = np.array([[0, 0, 0] for i in range(3)])


def aktualny_gracz_f():
    return aktualny_gracz


def get_plansza():
    return plansza.copy()


def set_plansza(new_plansza):
    global plansza
    plansza = new_plansza


def wykonaj_ruch(x, y, gracz):
    plansza = get_plansza()
    if plansza[x][y] != 0:
        return "pole zajete"
    else:
        plansza[x][y] = gracz
        set_plansza(plansza)
    return "udalo sie"


def zmien_gracza():
    global aktualny_gracz
    aktualny_gracz = (-1) * aktualny_gracz


def tlumacz_na_x_y(ruch):
    if ruch == 1:
        return 0, 0
    if ruch == 2:
        return 0, 1
    if ruch == 3:
        return 0, 2
    if ruch == 4:
        return 1, 0
    if ruch == 5:
        return 1, 1
    if ruch == 6:
        return 1, 2
    if ruch == 7:
        return 2, 0
    if ruch == 8:
        return 2, 1
    if ruch == 9:
        return 2, 2
    else:
        return None

def czy_koniec_2():
    #Sprawdz kolumny
    global flaga_who_win
    flaga_who_win = 1
    #zwróci 0 gdy 1 gracz wygra
    #zwroci 2 gdy 2 gravz wygra
    #zwroci 1 gdy remis
    if (plansza[0][0] == 1 and plansza[1][0] == 1 and plansza[2][0] == 1 or
            plansza[0][1] == 1 and plansza[1][1] == 1 and plansza[2][1] == 1 or
            plansza[0][2] == 1 and plansza[1][2] == 1 and plansza[2][2] == 1 or
            plansza[0][0] == 1 and plansza[0][1] == 1 and plansza[0][2] == 1 or
            plansza[1][0] == 1 and plansza[1][1] == 1 and plansza[1][2] == 1 or
            plansza[2][0] == 1 and plansza[2][1] == 1 and plansza[2][2] == 1 or
            plansza[0][0] == 1 and plansza[1][1] == 1 and plansza[2][2] == 1 or
            plansza[2][0] == 1 and plansza[1][1] == 1 and plansza[0][2] == 1 ):
        flaga_who_win = 0
    elif (plansza[0][0] == -1 and plansza[1][0] == -1 and plansza[2][0] == -1 or
            plansza[0][1] == -1 and plansza[1][1] == -1 and plansza[2][1] == -1 or
            plansza[0][2] == -1 and plansza[1][2] == -1 and plansza[2][2] == -1 or
            plansza[0][0] == -1 and plansza[0][1] == -1 and plansza[0][2] == -1 or
            plansza[1][0] == -1 and plansza[1][1] == -1 and plansza[1][2] == -1 or
            plansza[2][0] == -1 and plansza[2][1] == -1 and plansza[2][2] == -1 or
            plansza[0][0] == -1 and plansza[1][1] == -1 and plansza[2][2] == -1 or
            plansza[2][0] == -1 and plansza[1][1] == -1 and plansza[0][2] == -1 ):
        flaga_who_win = 2

    if flaga_who_win == 0:
        return 0
    elif flaga_who_win == 2:
        return 2
    elif flaga_who_win == 1:
        return 1


    # Sprawdz wiersze

    # Sprawdz po ukosie

def czy_koniec():
    for i in range(3):
        if plansza[i][0] == plansza[i][1] and plansza[i][2] == plansza[i][1] and plansza[i][2] != 0:
            return plansza[i][0]
    for i in range(3):
        if plansza[0][i] == plansza[1][i] and plansza[2][i] == plansza[1][i] and plansza[2][i] != 0:
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
            elif plansza[i][j] == -1:
                wyglad += "X"
    print('Wygląd planszy:',wyglad)
    return wyglad




def nasluchuj(client):
    msg = ''
    data = True
    while data:
        data = client.recv(1)
        print('I receive = ' + data.decode('utf-8'))
        msg += data.decode('utf-8')
        if msg[-4:] == '\r\n\r\n':
            break
    print(msg)
    return msg


#Funkcja do obslugi wszystkich błędów (msg) albo kod błędu



def create_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=r'C:\Users\admin\Downloads\selfsigned.crt',
                            keyfile=r'C:\Users\admin\Downloads\private.key')
    context.load_verify_locations(cafile=r'C:\Users\admin\Downloads\selfsigned.crt')

    return context


context = create_context()

dictionary_data_users = {}


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, numer_gracza, session_id):
        print("startuje")
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.numer_gracza = numer_gracza
        self.session_id = session_id

    def run(self):
        while True:
            resp = None
            #resp = self.csocket.recv(2000)
            resp = nasluchuj(self.csocket)
            #resp = resp.decode()
            print(resp)
            if resp[:len('To:SER\r\nLogin')] == 'To:SER\r\nLogin':
                login = resp[14:17]
                global dictionary_data_users
                dictionary_data_users[login] = {
                    "session_id": self.session_id,
                    "numer_gracza": self.numer_gracza
                }
                message = resp[45:-4]

                if message == "START":
                    mess = f'To:{login}\r\nsession_number:{self.session_id}\r\n\r\n'
                    self.csocket.sendall(mess.encode())
                    #                     resp = nasluchuj(self.csocket)
                    #resp = self.csocket.recv(2000)
                    #resp = resp.decode()
                    resp = nasluchuj(self.csocket)

                    if resp[-19:-4] != "BAD CREDENTIALS":
                        msg = odpakuj(resp)
                        To, From, Information_about_client_sesion_id, Message_id, Content_length, msg = msg
                        print(To)
                        print(msg)
                        print(From,str(login))
                        print(Information_about_client_sesion_id,type(Information_about_client_sesion_id))
                        print(self.session_id)
                        if "SER" == To and str(login) == From and Information_about_client_sesion_id == str(self.session_id):
                            #msg = Message
                            print('Jestem w pętli')
                            print(msg)
                            print(msg[:len("i am ready")] in "i am ready")
                            if msg in "i am ready":

                                while True:
                                    if aktualny_gracz != self.numer_gracza:
                                        #print(aktualny_gracz)
                                        pass
                                    else:
                                        print("jestem tutaj 1")
                                        # Sprawdzam która gra się skończyła i wysyłam do jednego i drugiego klienta informacje o tym
                                        if czy_koniec() == 1:
                                            msg = opakuj(login, "SER", self.session_id, 200, len("YOU WIN PLAYER 0"),
                                                         "YOU WIN PLAYER 1")
                                            self.csocket.sendall(msg.encode())
                                        elif czy_koniec() == -1:
                                            zmien_gracza()
                                            msg = opakuj(login, "SER", self.session_id, 200, len("YOU WIN PLAYER 0"),
                                                         "YOU WIN PLAYER -1")
                                            self.csocket.sendall(msg.encode())
                                        # Jeśli gra się nie skończyła
                                        else:
                                            # Wyślij wiadomość do gracza  aby podał ruch wraz z aktualnym stanem planszy
                                            msg_podaj_ruch = opakuj(login, "SER", self.session_id, 200,
                                                                    len("PODAJ RUCH"+podaj_wyglad_planszy()), "PODAJ RUCH"+ podaj_wyglad_planszy())
                                            self.csocket.sendall(msg_podaj_ruch.encode())
                                            # Czeka na ruch klienta
                                            #                                             resp = nasluchuj(self.csocket)
                                            #resp = self.csocket.recv(2000)
                                            #resp = resp.decode()
                                            resp = nasluchuj(self.csocket)
                                            msg = odpakuj(resp)
                                            To, From, Information_about_client_sesion_id, Message_id, Content_length, msg = msg
                                            print(msg[0:-1])
                                            if msg[0:-1] == "RUCH":
                                                ruch = int(msg[4:5])
                                                print('Ruch: ', ruch)

                                            #ruch = int(resp[-5:-4])
                                            if ruch >= 1 and ruch <= 9:
                                                x, y = tlumacz_na_x_y(ruch)
                                                czy_udalo_sie = wykonaj_ruch(x, y, aktualny_gracz)
                                                if czy_udalo_sie == "pole zajete":
                                                    msg_zly_ruch = opakuj(login, "SER", self.session_id, 400,
                                                                          len("BAD MOVE"), "BAD MOVE")
                                                    self.csocket.sendall(msg_zly_ruch.encode())
                                                elif czy_udalo_sie == "udalo sie":
                                                    msg_dobry_ruch = opakuj(login, "SER", self.session_id, 400,
                                                                            len("RIGHT MOVE"), "RIGHT MOVE")
                                                    self.csocket.sendall(msg_dobry_ruch.encode())
                                                    # Dobry ruch więc muszę zmienić gracza i powtórzyć pętle

                                                    zmien_gracza()

                                            # zwaliduj czy wiadomość jaka otrzymałeś jest ruchem czy jest to int od 1-9

                                #### serwer sprawdza czy gra się nie skończyła i jeżeli się skończyła to informuje gracza jeżeli nie to:
                                #### serwer wysyła wiadomość do gracza by podał ruch
                                #### i przetwarza ten ruch, sprawdza czy legalny informuje że się powiódł ( lub że się nie powiódł)
                                #### zmienić aktualnego gracza
                                ####


LOCALHOST = "127.0.0.1"
PORT = 8082

licznik_graczy = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', PORT))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:

        print("Server started")
        print(podaj_wyglad_planszy())
        while True:
            if licznik_graczy < 2:
                clientsock, clientAddress = ssock.accept()

                Session_id = int(uuid.uuid4())
                print("Session id: ", Session_id)
                newthread = ClientThread(clientAddress, clientsock, aktualny_gracz_f(), Session_id)
                newthread.start()
                zmien_gracza()
                licznik_graczy += 1
