#Client
import ssl
import requests
import tkinter as tk

root = tk.Tk()
root.title("Tic Tac Toe")


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



import socket
SERVER = "127.0.0.1"
PORT = 8082
with socket.create_connection((SERVER,PORT)) as sock:

    with context.wrap_socket(sock, server_hostname="localhost") as client:
        print(client.version())
#         client.sendall(b"cos tam")
        print("connected")


        def New_game():

            def button_click(button):
                global bclick
                if button["text"] == " ":
                    button["text"] = 'X'
                    bclick = True
                    button["state"] = 'normal'
                    button["state"] = 'disabled'

            msg_start = "START"

            client.sendall(msg_start)

            #Czy mogę zacząć grę?


            od_serwera = client.recv(4024)

            if od_serwera == 'ok':

                print("Move to windowe where")
                window = tk.Toplevel(root)
                window.geometry("600x600")
                window['background'] = '#00ace6'

                label = tk.Label(window, text="Your name:", font='Helvetica', bg='#00ace6', fg='black', height=2, width=14)
                label.grid(row=1, column=0)

                p1 = tk.StringVar()
                player1_name = tk.Entry(window, textvariable=p1, bd=9)
                player1_name.grid(row=1, column=1, columnspan=2)

                button7 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button7))
                button7.grid(row=2, column=1)

                button8 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button8))
                button8.grid(row=2, column=2)

                button9 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button9))
                button9.grid(row=2, column=3)

                button4 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button4))
                button4.grid(row=3, column=1)

                button5 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button5))
                button5.grid(row=3, column=2)

                button6 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button6))
                button6.grid(row=3, column=3)

                button1 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button1))
                button1.grid(row=4, column=1)

                button2 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button2))
                button2.grid(row=4, column=2)

                button3 = tk.Button(window, text=" ", font='Times 20 bold', bg='white', fg='white', height=4, width=8,
                                    command=lambda: button_click(button3))
                button3.grid(row=4, column=3)

                # button_new_game = tk.Button(window, text="New game ", font='Times 20 bold', bg='white', height=4, width=8)
                # button_new_game.grid(row=5, column=3)
                # img_1 = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed_2.png")
                button_new_game = tk.Button(window, text="New game", bg='white', width=18, height=3, command=New_game)

                # img_1 = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed_2.png")
                # button_new_game.config(image=img_1)
                button_new_game.grid(row=2, column=0)

        b = tk.Button(root, text="New game", command=New_game)
        b.config(width=300, height=100)

        img = tk.PhotoImage(file="C:/Users/admin/Desktop/TICtacTOE/unnamed.png")
        b.config(image=img)
        b.pack(expand=1)

        while True:



            in_data =  client.recv(4024)
            print("From Server :" ,in_data.decode())
            out_data = str(input())
            client.sendall(out_data.encode())
            if out_data=='bye':
                break
        client.close()
