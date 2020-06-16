import ssl
import requests
import tkinter as tk
import uuid
import numpy as np

root = tk.Tk()
root.title("Tic Tac Toe")

aktualny_stan_planszy = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
root.geometry("600x600")

root['background'] = '#00ace6'

# requests.get("http://127.0.0.1", verify=r'C:\Users\admin\Downloads\server.crt')
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=r'C:\Users\admin\Downloads\selfsigned.crt')
context.load_cert_chain(certfile=r'C:\Users\admin\Downloads\selfsigned.crt', keyfile=r'C:\Users\admin\Downloads\private.key')


# context.load_verify_locations(cafile=r'C:\Users\admin\Downloads\client.crt')

# Tablica

# |7|8|9|
# |4|5|6|
# |1|2|3|

# Struktura wiadomości
# 'To:\r\n
# From:\r\n
# Information_about_client_sesion_id:\r\n
# Message_id:\r\n
# Content-length:\r\n
# Message:\r\n\r\n
def opakuj(To, From, Information_about_client_sesion_id, Message_id, Content_length, Message):
    return f"To:{To}\r\nFrom:{From}\r\nInformation_about_client_sesion_id:{Information_about_client_sesion_id:39}\r\nMessage_id:{Message_id:03}\r\nContent_length:{Content_length:03}\r\nMessage:{Message}"

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


# Funkcja nasłuchująca wiadomość od serwera
def nasluchuj_serwer(client):
    data = b""
    r = True
    while data:
        r = client.recv(1)
        print(r)
        data += r
    return data


# Będziemy wysyłać poszczególne cyfry poprzez ten sposób będziemy wiedzieć które pole skreślił klient

# Funkcja która będzie zmieniać stan buttona tak aby wyświetlić ruch otrzymany od serwera
# def change_state_button_from_server(button1,button2,button3,button4,button5,button6,button7,button8,button9,number):
#    pass
gra_rozpoczeta = False


def set_plansza(plansza):
    global aktualny_stan_planszy
    for znak in range(9):
        aktualny_stan_planszy[znak] = plansza[znak]


def button_click(button, number, aktualny_stan_planszy, list_of_button):
    global bclick
    if button["text"] == " ":
        button["text"] = 'X'
        bclick = True
        button["state"] = 'normal'
        button["state"] = 'disabled'
        aktualny_stan_planszy[number - 1] = "X"
        print(aktualny_stan_planszy)

        # Serwer czeka na ruch więc muszę mu wysłać aktualny stan planszy i ruch <- wystarczy że wyślesz numer ruch
        ruch = str(number)
        #         msg_stan_planszy_ruch= "".join(aktualny_stan_planszy)+"\n\n"+ruch
        client.sendall(ruch.encode())

        # Jeżeli ruch prawidłowy to sprawdź co mówi serwer
        # Czy koniec gry i jaki wynik - ok
        # ok2 - przyjął ruch ale gra jeszcze nie jest zakonczona
        # ok0
        # ok1 gra wygrana lub przerwana
        global gra_rozpoczeta
        if not gra_rozpoczeta:
            msg = b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode())
                msg += data
                if msg == b'i am ready':
                    break
            msg = b''
            client.sendall(b"START")
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode())
                msg += data
                if msg == b'ok':
                    gra_rozpoczeta = True
                    break

        if gra_rozpoczeta:
            msg = b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode())
                msg += data
                if msg == b'musisz poczekac':
                    msg = b""
                    print("czekam")
                    client.sendall(b"ok")
                    msg = b''
                    pass

                if msg[:10] == b"podaj ruch" and len(msg) == 19:
                    plansza = msg[10:]
                    plansza = plansza.decode()
                    for i in range(9):
                        if plansza[i] != " ":
                            list_of_button[i + 1]["text"] = plansza[i]
                            list_of_button[i + 1]["state"] = 'normal'
                            list_of_button[i + 1]["state"] = 'disabled'
                            aktualny_stan_planszy[i] = plansza[i]
                        client.sendall(ruch.encode())
                    print("wykonałem ruch")
                    break
            msg = b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode())

                msg += data
                print(msg)
                if (msg == b'nieprawidlowy ruch'):
                    button["text"] = ' '
                    bclick = False
                    button["state"] = 'normal'
                    aktualny_stan_planszy[number - 1] = " "
                    return
                if (msg == b'ok1'):
                    print("Wygrana")
                    return
                elif (msg == b'ok0'):
                    print("Przegrana")
                    return
                elif (msg == b'ok2'):
                    # Gra toczy się dalej
                    # odczytaj ruch
                    # Tutaj najlepiej jakby serwer wysłał numer(numer potrzebny do zaktualizowania planszy)wtedy:
                    # Jeśli wysłał ok2 to powinien wysłać numer ruchu

                    msg = client.recv(1)
                    msg = int(msg.decode())
                    number_button_from_server = msg
                    list_of_button[number_button_from_server]['text'] = 'O'
                    list_of_button[number_button_from_server]["state"] = 'normal'
                    list_of_button[number_button_from_server]["state"] = 'disabled'
                    aktualny_stan_planszy[number_button_from_server - 1] = "O"

                    break

                    break


def New_game():
    global aktualny_stan_planszy

    aktualny_stan_planszy = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    msg_start = "START"

    login = np.random.randint(100, 999)

    msg_start = f'To:Server\r\nLogin:{login}\r\nContent-length:5\r\nMessage:START\r\n\r\n'

    client.sendall(msg_start.encode())

    # client.sendall(msg_start.encode())

    # Czy mogę zacząć grę?

    # od_serwera = client.recv(4024)

    od_serwera = 'ok'


import socket

SERVER = "127.0.0.1"
PORT = 8082
with socket.create_connection((SERVER, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname="localhost") as client:
        session_id = None
        while True:
            command = str(input("podaj komendę"))
            if command == "start":
                login = np.random.randint(100, 999)
                msg_start = f'To:SER\r\nLogin:{login}\r\nContent-length:5\r\nMessage:START\r\n\r\n'
                client.sendall(msg_start.encode())
                print(msg_start)
                resp = None
                resp = client.recv(1000)
                resp = resp.decode()
                print("test -1 ")
                print(resp)

                if resp != "code:400 login failed":
                    print(resp[3:6], type(resp[3:6]), len(resp[3:6]))
                    print(str(login), type(str(login)), len(str(login)))
                    int_resp = int(resp[3:6])
                    int_login = int(login)
                    if int_login == int_resp:
                        print('1')
                    if int_login == int_resp:
                        print('Jestem tu')
                        session_id = resp[23:-4]
                        print(session_id)
                        msg = opakuj("SER", login, session_id, 100, len("i am ready"), "i am ready")
                        client.sendall(msg.encode())
                        print("tutaj")
                        while True:
                            resp = client.recv(1000)
                            print(resp)
                            resp = resp.decode()

                            print('check')
                            if resp != "code:401 Timeout":# zmieńmy to może na to że jak nie dostaniejsz odpowiedzi w ciągu x sekund to masz timeout
                                print('check 1')
                                print(resp)
                                msg = odpakuj(resp)
                                To, From, Information_about_client_sesion_id, Message_id, Content_length, msg = msg
                                if To == str(login) and session_id == str(Information_about_client_sesion_id): # nie wiem czy chcemy sprawdzać swoje session_id
                                    print(msg[-9:])
                                    print('check 2')

                                    command = str(input("Podaj ruch:"))
                                    ruch = "RUCH"+ command
                                    #Tutaj urzytkownik poda ruch i wyśle liczbę, serwer zwaliduje czy była ona poprawna
                                    msg_ruch = opakuj("SER",login,session_id,100,len(ruch),ruch)
                                    client.sendall(msg_ruch.encode())
                                    print('check 2')
                                    #Czekaj na odpowiedz serwera o ruchu
                                    resp = client.recv(1000)
                                    resp = resp.decode()
                                    if resp[3:6] == str(login) and session_id == resp[25:-4]:
                                        if resp[-12:-4] == "BAD MOVE":
                                            print("BAD MOVE")
                                        if resp[-14:-4] == "RIGHT MOVE":
                                            print("RIGHT MOVE")
                                            #Dobry ruch więc czekam na swoją kolej





                    else:
                        msg = f'To:Server\r\nLogin:{login}\r\nContent-length:5\r\nMessage:BAD CREDENTIALS\r\n\r\n'
                        client.sendall(msg.encode())
                else:
                    print("nie powiodło się logowanie")

        client.close()
