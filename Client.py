import socket
import sys
import os
import tkinter as tk
from tkinter import ttk,Entry
ip = "127.0.0.1"
port = 3839

def tryConnecting(username,password):
    # Let's try connecting through UDP protocol with username and password
    s.sendto(username.encode('utf-8'), (ip, port))
    s.sendto(password.encode('utf-8'), (ip, port))
    success, address = s.recvfrom(1024)
    
    if success.decode("utf-8") == "Success":
        quit()
    else :
        addWrongAuthentification()


def login():
    global window
    window = tk.Tk()
    
    window.title("Login")
    window.geometry("400x400")
    
    username = tk.StringVar()
    password = tk.StringVar()

    def loginCommand():
        print(username.get())
        tryConnecting(username.get(), password.get())

    tk.Label(window,text='User name:').place(x=85,y=170)
    tk.Label(window,text='Password:').place(x=85,y=220)
    
    username_entry=tk.Entry(window,textvariable=username)
    username_entry.place(x=150,y=170)

    password_entry=tk.Entry(window,textvariable=password)
    password_entry.place(x=150,y=220)

    login_button=tk.Button(window,text='Login',command=loginCommand)
    login_button.place(x=180,y=250)

    window.mainloop()

def addWrongAuthentification():
    ttk.Label(window, text = 'Wrong username or password.. Try again' ).place(x=100,y=20)

def close():
        s.close()

def quit():
        window.destroy()

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

#start the login interface
login()
