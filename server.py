# SERWER
import ssl
import uuid

import numpy as np
import socket, threading
import time


def opakuj(To, From, Information_about_client_sesion_id, Message_id, Content_length, Message):
    return f"To:{To}\r\nFrom:{From}\r\nInformation_about_client_sesion_id:{Information_about_client_sesion_id}\r\nMessage_id:{Message_id}\r\n\Content_length\r\n{Content_length}\r\nMessage{Message}"


def read_message(message):
    # Tutaj można odbierać wiadomość dopóki b'\r\n\r\n' not in data
    # data = b''
    # while b'\r\n\r\n' not in data:
    #    data += client.recv(1)
    To = message[message[0:].find("To:") + 3:message.find('\r\nFrom:')]
    From = message[message[0:].find("From:") + 5:message.find('\r\nInformation_about_client_sesion_id:')]
    Information_about_client_sesion_id = message[
                                         message[0:].find("Information_about_client_sesion_id:") + 35:message.find(
                                             '\r\nMessage_id:')]
    Message_id = message[message[0:].find("Message_id:") + 11:message.find('\r\nContent-length:')]
    Content_length = int(message[message[0:].find("Content-length:") + 15:message.find('\r\nMessage:')])
    # len = 8+Content_length
    Message = message[message[0:].find("Message:") + 8:message.find('\r\n\r\n')]

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
            else:
                wyglad += "X"
    return wyglad


def nasluchuj(socket):
    data = b''
    while data:
        #może tutaj powinniśmy dać socket na który ma nasłuchiwać?
        data += socket.recv(1)
        print(data)
    return data



wykonaj_ruch(2, 1, 1)


# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain(r'C:\Users\patryk.krawczak\Downloads\server.crt', r'C:\Users\patryk.krawczak\Downloads\server.key')
def create_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=r'C:\Users\admin\Downloads\server.crt',
                            keyfile=r'C:\Users\admin\Downloads\server.key')
    context.load_verify_locations(cafile=r'C:\Users\admin\Downloads\client.crt')

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
            resp = nasluchuj(self.csocket)
            resp = resp.decode()
            print(resp)
            if resp[:16] == 'To:Server\r\nLogin':
                login = resp[16:20]
                global dictionary_data_users
                dictionary_data_users[login] = {
                    "session_id": self.session_id,
                    "numer_gracza": self.numer_gracza
                }
                message = resp[48:-4]

                if message == "START":
                    mess = f'To:{login}\r\nsession_number:{self.session_id}\r\n\r\n'
                    self.csocket.sendall(mess.encode())
                    resp = nasluchuj()
                    resp = resp.decode()
                    if resp[-19:-4] != "BAD CREDENTIALS":
                        msg = read_message(resp)
                        To, From, Information_about_client_sesion_id, Message_id, Content_length, Message = msg
                        if To == "SERWER" and From == str(login) and Information_about_client_sesion_id == str(
                                self.session_id):
                            msg = Message
                            if msg == "i am ready":
                                while True:
                                    if aktualny_gracz != self.numer_gracza:
                                        pass
                                    else:
                                        #Sprawdzam która gra się skończyła i wysyłam do jednego i drugiego klienta informacje o tym
                                        if czy_koniec() == 0:
                                            msg = opakuj(login,"SERWER",self.session_id,200,len("YOU WIN PLAYER 0" ),"YOU WIN PLAYER 0")
                                            self.csocket.sendall(msg.encode())
                                        elif czy_koniec() == 2:
                                            zmien_gracza()
                                            msg = opakuj(login, "SERWER", self.session_id, 200, len("YOU WIN PLAYER 0"),"YOU WIN PLAYER 0")
                                            self.csocket.sendall(msg.encode())
                                        #Jeśli gra się nie skończyła
                                        else:
                                            #Wyślij wiadomość do gracza  aby podał ruch wraz z aktualnym stanem planszy
                                            msg_podaj_ruch = opakuj(login, "SERWER", self.session_id, 200, len("PODAJ RUCH"),"PODAJ RUCH")
                                            self.csocket.sendall(msg_podaj_ruch.encode())
                                            #Czeka na ruch klienta
                                            resp = nasluchuj()
                                            resp = resp.decode()
                                            ruch = int(resp[-5:-4])
                                            if ruch >=1 and ruch <=9:
                                                x,y = tlumacz_na_x_y(ruch)
                                                czy_udalo_sie = wykonaj_ruch(x,y,self.csocket)
                                                if czy_udalo_sie == "pole zajete":
                                                    msg_zly_ruch = opakuj(login,"SERWER",self.session_id,400,len("BAD MOVE"),"BAD MOVE")
                                                    self.csocket.sendall(msg_zly_ruch.encode())
                                                elif czy_udalo_sie == "udalo sie":
                                                    msg_dobry_ruch = opakuj(login, "SERWER", self.session_id, 400,len("RIGHT MOVE"), "RIGHT MOVE")
                                                    self.csocket.sendall(msg_dobry_ruch.encode())
                                                    #Dobry ruch więc muszę zmienić gracza i powtórzyć pętle
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
        while True:
            if licznik_graczy < 2:
                clientsock, clientAddress = ssock.accept()
                Session_id = int(uuid.uuid4())
                newthread = ClientThread(clientAddress, clientsock, aktualny_gracz_f(), Session_id)
                newthread.start()
                zmien_gracza()
                licznik_graczy += 1

## CLIENT