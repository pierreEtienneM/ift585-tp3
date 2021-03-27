import tkinter as tk
from tkinter import ttk,Entry
import requests

def mainPage(username, userId):
    window = tk.Tk()
    
    window.title("Main")
    window.geometry("400x400")

    def profileCommand():
        response = requests.get("http://127.0.0.1:5000/folders")
        #faire un redirigiment de page

    def inviteCommand():
        response = requests.get("http://127.0.0.1:5000/users/{0}/invites".format(userId))
        #faire un redirigiment de page

    ttk.Label(window, text = 'Hello, ' + username).place(x=170,y=0)

    login_button=tk.Button(window,text='My Profile',command=profileCommand)
    login_button.place(x=120,y=170)

    login_button=tk.Button(window,text='My Invites',command=inviteCommand)
    login_button.place(x=190,y=170)

    window.mainloop()