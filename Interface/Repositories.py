import tkinter as tk
from tkinter import ttk, Entry, filedialog
import requests

def mainPage(folderId):
    window = tk.Tk()
    
    window.title("Répertoires")
    window.geometry("400x400")

    label = ttk.Label(window, text = 'Mes répertoires')
    label.pack()

    def selectAndSendFile():
        filename = filedialog.askopenfilename(initialdir=".",title="Selectionnez un fichier")
        url = "http://127.0.0.1:5000/folders/" + str(folderId) + "/newfile"
        files = {'file': open(filename ,'rb')}
        data = {
            'folderId': folderId
        }
        response = requests.post(url, files=files, data=data).json()

        print(response["success"])
        print(response["message"])

    tk.Button(window, text ="Envoyer un fichier", command = selectAndSendFile).pack()

    window.mainloop()

mainPage(1)