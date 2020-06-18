import ssl
import requests
import tkinter as tk
import uuid
import numpy as np
import pygame
from grid import Grid
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '850,100'

surface = pygame.display.set_mode((600,700))
pygame.display.set_caption('Tic-tac-toe')

aktualny_stan_planszy = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


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
    return f"To:{To}\r\nFrom:{From}\r\nInformation_about_client_sesion_id:{Information_about_client_sesion_id:39}\r\nMessage_id:{Message_id:03}\r\nContent_length:{Content_length:03}\r\nMessage:{Message}\r\n\r\n"

def dekoduj_wygląd(string,grid):
    licznik = 0
    #plansza =  [[" ", " ", " "] for i in range(3)]
    for j in range(3):
        for i in range(3):
            if string[licznik]==" ":
                #plansza[i][j] = " "
                grid.set_cell_value(i,j,0)
            elif string[licznik] == "O":
                #plansza[i][j] = "O"
                grid.set_cell_value(i, j, "O")
            elif string[licznik] == "X":
                #plansza[i][j] = "X"
                grid.set_cell_value(i, j, "X")
            licznik += 1
    #for i in plansza:
    #    print("|".join(i))
    return grid

def odpakuj(msg):
    #for i in msg:
    #    print([i])
    to = msg[3:6]
    From = msg[13:16]
    Info_id = msg[53:92]
   # print("Odpakuj: ", Info_id)
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
def nasluchuj_serwer(serwer):
    msg = ''
    data = True
    while data:
        data = serwer.recv(1)
        #print('I receive = ' + data.decode('utf-8'))
        msg += data.decode('utf-8')
        if msg[-4:] == '\r\n\r\n':
            break
    #print(msg)
    return msg


# Będziemy wysyłać poszczególne cyfry poprzez ten sposób będziemy wiedzieć które pole skreślił klient

# Funkcja która będzie zmieniać stan buttona tak aby wyświetlić ruch otrzymany od serwera
# def change_state_button_from_server(button1,button2,button3,button4,button5,button6,button7,button8,button9,number):
#    pass
gra_rozpoczeta = False


def set_plansza(plansza):
    global aktualny_stan_planszy
    for znak in range(9):
        aktualny_stan_planszy[znak] = plansza[znak]

# |7|8|9|
# |4|5|6|
# |1|2|3|


def translate_pos_to_number(pos_x,pos_y):
    t = np.array([[0, 0, 0] for i in range(3)])
    t[0][0] = 1
    print(t)
    print("transalepos: ",pos_x,pos_y)
    if pos_x == 0 and pos_y == 0 :
        return 7
    elif pos_x == 0 and pos_y == 1:
        return  8
    elif pos_x == 0 and pos_y == 2:
        return  9
    elif pos_x == 1 and pos_y == 2:
        return  6
    elif pos_x == 1 and pos_y == 1:
        return  5
    elif pos_x == 1 and pos_y == 0:
        return  4
    elif pos_x == 2 and pos_y == 0:
        return  1
    elif pos_x == 2 and pos_y == 1:
        return  2
    elif pos_x == 2 and pos_y == 2:
        return  3
    elif pos_x == 1 and pos_y == 3:
        return "start"



#Funkcja do obslugi wszystkich błędów (msg) albo kod błędu

import socket

pygame.init()
grid = Grid()
running = True
playing = 'True'
font = pygame.font.SysFont("comicsansms", 72)
text_win = font.render("You Win", True, (0, 0, 0))
text_lose = font.render("You Lose", True, (0, 0, 0))
text_draw = font.render("Draw", True, (0, 0, 0))

SERVER = "127.0.0.1"
PORT = 8081

plansza = " " * 9

with socket.create_connection((SERVER, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname="localhost") as client:
        session_id = None
        while True:
            #command = str(input("Podaj komendę"))
            #command = translate_pos_to_number(pos[0] // 200, pos[1] // 200)
            czy_wyjsc = True
            while czy_wyjsc:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:  # [0] Jeśli lewy przycisk myszki jest kliknięty
                            pos = pygame.mouse.get_pos()
                            print(pos[0] // 200, pos[1] // 200)
                            czy_wyjsc = False
                            break
                surface.fill((20, 189, 172))

                grid.draw(surface)

                pygame.display.flip()

            if (pos[0] // 200 == 1, pos[1] // 200 == 3):
                command = "start"
                if command == "start":
                    login = np.random.randint(100, 999)
                    msg_start = f'To:SER\r\nLogin:{login}\r\nContent-length:5\r\nMessage:START\r\n\r\n'
                    client.sendall(msg_start.encode())
                    #print(msg_start)
                    resp = None
                    #resp = client.recv(1000)
                    #resp = resp.decode()
                    resp = nasluchuj_serwer(client)
                    #print("test -1 ")
                    #print(resp)

                    if resp != "code:400 login failed":
                        #print(resp[3:6], type(resp[3:6]), len(resp[3:6]))
                        #print(str(login), type(str(login)), len(str(login)))
                        int_resp = int(resp[3:6])
                        int_login = int(login)
                        if int_login == int_resp:
                            #print('1')
                            pass
                        if int_login == int_resp:
                            #print('Jestem tu')
                            session_id = resp[23:-4]
                            #print(session_id)
                            msg = opakuj("SER", login, session_id, 100, len("i am ready"), "i am ready")
                            client.sendall(msg.encode())
                            #print("tutaj")
                            while True:
                                #resp = client.recv(1000)
                                #print(resp)
                                #resp = resp.decode()
                                resp = nasluchuj_serwer(client)
                                #print('check')
                                if resp != "code:401 Timeout":# zmieńmy to może na to że jak nie dostaniejsz odpowiedzi w ciągu x sekund to masz timeout
                                    #print('check 1')
                                    #print(resp)
                                    msg = odpakuj(resp)
                                    To, From, Information_about_client_sesion_id, Message_id, Content_length, msg = msg

                                    if To == str(login) and session_id == str(Information_about_client_sesion_id): # nie wiem czy chcemy sprawdzać swoje session_id
                                        #print(msg[0:14])
                                        #print('Cale msg',msg)
                                        #Podzielić tak jak wygląda plansza
                                        #print('check 2')
                                        #print(Message_id=='200')
                                        #print(msg[0:14]=='YOU WIN PLAYER')
                                        if msg[0:10] == 'PODAJ RUCH':
                                            plansza = msg[10:]
                                            print('Plansza1:',plansza)
                                            #dekoduj_wygląd(msg[10:])
                                            #command = str(input("Podaj ruch:"))
                                            print('tutaj')
                                            czy_wyjsc = True
                                            while czy_wyjsc:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        running = False
                                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                                        if pygame.mouse.get_pressed()[
                                                            0]:  # [0] Jeśli lewy przycisk myszki jest kliknięty
                                                            pos = pygame.mouse.get_pos()
                                                            print(pos[0] // 200, pos[1] // 200)
                                                            grid = dekoduj_wygląd(plansza,grid)
                                                            czy_wyjsc = False
                                                            break
                                                surface.fill((20, 189, 172))
                                                grid = dekoduj_wygląd(plansza,grid)
                                                #grid.set_cell_value(pos[0] // 200, pos[1] // 200)
                                                grid.draw(surface)

                                                pygame.display.flip()

                                            print(pos)

                                            command = translate_pos_to_number(pos[0] // 200, pos[1] // 200)
                                            print(command)
                                            ruch = "RUCH"+ str(command)
                                            #Tutaj urzytkownik poda ruch i wyśle liczbę, serwer zwaliduje czy była ona poprawna
                                            msg_ruch = opakuj("SER",login,session_id,100,len(ruch),ruch)
                                            client.sendall(msg_ruch.encode())
                                            print('wchodze')
                                            #print('check 2')
                                            #Czekaj na odpowiedz serwera o ruchu
                                            #resp = client.recv(1000)
                                            #resp = resp.decode()

                                            resp = nasluchuj_serwer(client)
                                            #print(resp[3:6]==str(login))
                                            wiad = odpakuj(resp)
                                            To, From, Information_about_client_sesion_id, Message_id, Content_length, msg = wiad
                                            print(msg[0:10])
                                            #print(Information_about_client_sesion_id == session_id)
                                            #print(session_id == resp[25:-4])
                                            if resp[3:6] == str(login) and session_id == Information_about_client_sesion_id:
                                                if msg[0:10] == "BAD MOVE":
                                                    print("BAD MOVE")
                                                if msg[0:10] == "RIGHT MOVE":
                                                    print("RIGHT MOVE")
                                                    print('caly message',msg)
                                                    print('Plansza',msg[10:])
                                                    plansza_own_move = msg[10:]
                                                    grid = dekoduj_wygląd(plansza_own_move, grid)
                                                    grid.draw(surface)

                                                    pygame.display.flip()
                                                    #Dobry ruch więc czekam na swoją kolej

                                        elif msg[0:7] == 'YOU WIN' and Message_id == '200':
                                            print('You Win')
                                            plansza_own_move = msg[7:]
                                            grid = dekoduj_wygląd(plansza_own_move, grid)
                                            textSurface = font.render('You Win', True, (0, 0, 0))
                                            largeText = pygame.font.Font('freesansbold.ttf', 115)
                                            TextSurf = pygame.font.render('You Win', True, (0, 0, 0))
                                            TextRect = textSurface.get_rect()
                                            TextRect.center = ((600 / 2), (700 // 2))
                                            surface.blit(TextSurf, TextRect)
                                            grid.draw(surface)

                                            pygame.display.flip()
                                            break
                                        elif msg[0:8] == 'YOU LOSE' and Message_id == '200':
                                            print('You Lose')
                                            plansza_own_move = msg[8:]
                                            grid = dekoduj_wygląd(plansza_own_move, grid)

                                            grid.draw(surface)

                                            pygame.display.flip()
                                            break
                                        elif msg[0:30]=='YOU WI....OHHH SORRY. YOU DRAW' and Message_id == '200':
                                            print('DRAW')
                                            plansza_own_move = msg[30:]
                                            grid = dekoduj_wygląd(plansza_own_move, grid)
                                            grid.draw(surface)

                                            pygame.display.flip()
                                            break






                    else:
                        msg = f'To:Server\r\nLogin:{login}\r\nContent-length:5\r\nMessage:BAD CREDENTIALS\r\n\r\n'
                        client.sendall(msg.encode())
                else:
                    print("nie powiodło się logowanie")

        client.close()
surface.fill((20, 189, 172))

grid.draw(surface)

pygame.display.flip()
