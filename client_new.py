import ssl
import requests
import tkinter as tk

root = tk.Tk()
root.title("Tic Tac Toe")

aktualny_stan_planszy = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
root.geometry("600x600")

root['background'] = '#00ace6'

bclick = False

# requests.get("http://127.0.0.1", verify=r'C:\Users\patryk.krawczak\Downloads\server.crt')
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile = r'C:\Users\patryk.krawczak\Downloads\server.crt')
context.load_cert_chain(certfile= r'C:\Users\patryk.krawczak\Downloads\client.crt', keyfile= r'C:\Users\patryk.krawczak\Downloads\client.key')
# context.load_verify_locations(cafile=r'C:\Users\patryk.krawczak\Downloads\client.crt')

#Tablica

#|7|8|9|
#|4|5|6|
#|1|2|3|

#Będziemy wysyłać poszczególne cyfry poprzez ten sposób będziemy wiedzieć które pole skreślił klient

#Funkcja która będzie zmieniać stan buttona tak aby wyświetlić ruch otrzymany od serwera
#def change_state_button_from_server(button1,button2,button3,button4,button5,button6,button7,button8,button9,number):
#    pass
gra_rozpoczeta = False
def set_plansza(plansza):
    global aktualny_stan_planszy
    for znak in range(9):
        aktualny_stan_planszy[znak] = plansza[znak]

def button_click(button,number,aktualny_stan_planszy,list_of_button):
    global bclick
    if button["text"] == " ":
        button["text"] = 'X'
        bclick = True
        button["state"] = 'normal'
        button["state"] = 'disabled'
        aktualny_stan_planszy[number-1] = "X"
        print(aktualny_stan_planszy)

        #Serwer czeka na ruch więc muszę mu wysłać aktualny stan planszy i ruch <- wystarczy że wyślesz numer ruch
        ruch = str(number)
#         msg_stan_planszy_ruch= "".join(aktualny_stan_planszy)+"\n\n"+ruch
        client.sendall(ruch.encode())

        #Jeżeli ruch prawidłowy to sprawdź co mówi serwer
        #Czy koniec gry i jaki wynik - ok
        #ok2 - przyjął ruch ale gra jeszcze nie jest zakonczona
        #ok0
        #ok1 gra wygrana lub przerwana
        global gra_rozpoczeta
        if not gra_rozpoczeta:
            msg =b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode() )
                msg += data
                if msg == b'i am ready':
                    break
            msg =b''
            client.sendall(b"START")
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode() )
                msg += data
                if msg == b'ok':
                    
                    gra_rozpoczeta = True
                    break
                
        if gra_rozpoczeta:
            msg =b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode() )
                msg += data
                if msg == b'musisz poczekac':
                    msg = b""
                    print("czekam")
                    client.sendall(b"ok")
                    msg =b''
                    pass
                
                if msg[:10] == b"podaj ruch" and len(msg) == 19:
                    plansza = msg[10:]
                    plansza = plansza.decode()
                    for i in range(9):
                        if plansza[i]!= " ":
                            list_of_button[i+1]["text"] = plansza[i]
                            list_of_button[i+1]["state"] = 'normal'
                            list_of_button[i+1]["state"] = 'disabled'
                            aktualny_stan_planszy[i] = plansza[i]
                        client.sendall(ruch.encode())
                    print("wykonałem ruch")
                    break
            msg =b''
            while True:
                data = client.recv(1)
                print("I receive:" + data.decode() )
                
                msg += data
                print(msg)
                if(msg == b'nieprawidlowy ruch'):
                    button["text"] = ' '
                    bclick = False
                    button["state"] = 'normal'
                    aktualny_stan_planszy[number-1] = " "
                    return
                if(msg == b'ok1'):
                    print("Wygrana")
                    return
                elif(msg == b'ok0'):
                    print("Przegrana")
                    return
                elif(msg==b'ok2'):
                    #Gra toczy się dalej
                    #odczytaj ruch
                    #Tutaj najlepiej jakby serwer wysłał numer(numer potrzebny do zaktualizowania planszy)wtedy:
                    #Jeśli wysłał ok2 to powinien wysłać numer ruchu

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

    #client.sendall(msg_start.encode())

    # Czy mogę zacząć grę?

    #od_serwera = client.recv(4024)

    od_serwera = 'ok'

    if od_serwera == 'ok':
        #client.sendall("Startuje")

        print("Move to window where")
        window = tk.Toplevel(root)
        window.geometry("600x600")
        window['background'] = '#00ace6'

        label = tk.Label(window, text="Your name:", font='Helvetica', bg='#00ace6', fg='black', height=2, width=14)
        label.grid(row=1, column=0)

        p1 = tk.StringVar()
        player1_name = tk.Entry(window, textvariable=p1, bd=9)
        player1_name.grid(row=1, column=1, columnspan=2)

        button7 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button7,7,aktualny_stan_planszy,list_of_button))
        button7.grid(row=2, column=1)

        button8 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button8,8,aktualny_stan_planszy,list_of_button))
        button8.grid(row=2, column=2)

        button9 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button9,9,aktualny_stan_planszy,list_of_button))
        button9.grid(row=2, column=3)

        button4 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button4,4,aktualny_stan_planszy,list_of_button))
        button4.grid(row=3, column=1)

        button5 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button5,5,aktualny_stan_planszy,list_of_button))
        button5.grid(row=3, column=2)

        button6 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button6,6,aktualny_stan_planszy,list_of_button))
        button6.grid(row=3, column=3)

        button1 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button1,1,aktualny_stan_planszy,list_of_button))
        button1.grid(row=4, column=1)

        button2 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button2,2,aktualny_stan_planszy,list_of_button))
        button2.grid(row=4, column=2)

        button3 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                            command=lambda: button_click(button3,3,aktualny_stan_planszy,list_of_button))
        button3.grid(row=4, column=3)

        # button_new_game = tk.Button(window, text="New game ", font='Times 20 bold', bg='white', height=4, width=8)
        # button_new_game.grid(row=5, column=3)
        # img_1 = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed_2.png")
        button_new_game = tk.Button(window, text="New game", bg='white', width=18, height=3, command=New_game)

        # img_1 = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed_2.png")
        # button_new_game.config(image=img_1)
        button_new_game.grid(row=2, column=0)

        list_of_button = [button_new_game,button1,button2,button3,button4,button5,button6,button7,button8,button9]


import socket
SERVER = "127.0.0.1"
PORT = 8082
with socket.create_connection((SERVER,PORT)) as sock:

    with context.wrap_socket(sock, server_hostname="localhost") as client:
        print(client.version())
#         client.sendall(b"cos tam")
        print("connected")


        b = tk.Button(root, text="New game", command=New_game)
        b.config(width=300, height=100)

#         img = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed.png")
#         b.config(image=img)
        b.pack(expand=1)
        #root.update()
        root.mainloop()

        client.close()
