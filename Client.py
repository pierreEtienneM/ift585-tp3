import tkinter as tk
from tkinter import ttk, X, LEFT, RIGHT
import socket
import requests
import json

connected_userId = 0
connected_username = ""
LARGEFONT =("Verdana", 35)
MEDIUMFONT =("Verdana", 20)
IP = "127.0.0.1"
PORT = 3839
# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)



def showNavigation(frame, controller):
    navigationFrame = tk.Frame(frame)
    navigationFrame.pack(fill=X)

    def closeProgram():
        requests.post("http://127.0.0.1:5000/user/{0}/disconnect".format(connected_userId))
        controller.destroy()
    def disconnect():
        print(connected_userId)
        requests.post("http://127.0.0.1:5000/user/{0}/disconnect".format(connected_userId))
        controller.show_frame(LoginPage)

    homeButton = ttk.Button(navigationFrame, text ="Accueil",
        command = lambda : controller.show_frame(Home))
    homeButton.pack(side=LEFT, padx=5, pady=5)

    disconnectButton = ttk.Button(navigationFrame, text ="Me déconnecter", command = disconnect)
    disconnectButton.pack(side=RIGHT, padx=5, pady=5)

    controller.protocol("WM_DELETE_WINDOW", closeProgram)
    

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("IFT585Box")
        self.geometry("400x400")

        # Creation du conteneur de l'app
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # Initialisation du tableau de pages
        self.frames = {} 
  
        # Initialisation des pages de l'application
        for F in (LoginPage, Home, Repositories, Repository, Invites):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        # Affiche la page de login au lancement de l'application
        self.show_frame(LoginPage)
    
    # Affiche la page passee en parametre
    def show_frame(self, cont):
        frame = self.frames[cont]
        if "callinitrest" in dir(frame):
            frame.callinitrest()
        frame.tkraise()


# Page de login
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        username = tk.StringVar()
        password = tk.StringVar()

        def loginCommand():
            print(username.get())
            self.tryConnecting(controller, username.get(), password.get())

        tk.Label(self,text='User name:').place(x=85,y=170)
        tk.Label(self,text='Password:').place(x=85,y=220)
        
        username_entry=tk.Entry(self,textvariable=username)
        username_entry.place(x=150,y=170)

        password_entry=tk.Entry(self,textvariable=password)
        password_entry.place(x=150,y=220)

        login_button=tk.Button(self,text='Login',command=loginCommand)
        login_button.place(x=180,y=250)
    
    def tryConnecting(self, controller, username, password):
        # Let's try connecting through UDP protocol with username and password
        s.sendto(username.encode('utf-8'), (IP, PORT))
        s.sendto(password.encode('utf-8'), (IP, PORT))
        success, address = s.recvfrom(1024)
        
        if success.decode("utf-8") == "True":
            global connected_username
            global connected_userId
            connected_username, address = s.recvfrom(1024)
            connected_userId, address = s.recvfrom(1024)

            connected_username = connected_username.decode('utf-8')
            connected_userId = connected_userId.decode('utf-8')
            #TODO remove le label addWrongAuthentification quand on succeed sinon les label s'empile un par dessus l'autre

            controller.show_frame(Home)
        else :
            message, address = s.recvfrom(1024)
            self.addWrongAuthentification(message)

    def addWrongAuthentification(self,message):
        ttk.Label(self, text = message).place(x=130,y=20)
  

# Page d'accueil de l'utilisateur connecte
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        def repositoriesCommand():
            controller.show_frame(Repositories)

        def invitesCommand():
            controller.show_frame(Invites)
        #TODO pourquoi le username apparait pas, mais le userId fonctionne plus loin?
        ttk.Label(self, text = 'Bonjour, {0}'.format(connected_username)).place(x=170,y=0)

        login_button=tk.Button(self,text='Mes répertoire',command=repositoriesCommand)
        login_button.place(x=100,y=170)

        login_button=tk.Button(self,text='Mes invitations',command=invitesCommand)
        login_button.place(x=190,y=170)


# Page de la liste des repertoires auquel l'utilisateur connecte a acces
class Repositories(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        label = ttk.Label(self, text ="Mes répertoires", font = MEDIUMFONT)
        label.pack(side=LEFT, padx=5, pady=5)


# Page d'un repertoire qui liste les fichiers contenus
class Repository(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        label = ttk.Label(self, text ="Répertoire XXX", font = MEDIUMFONT)
        label.pack(side=LEFT, padx=5, pady=5)


# Page qui liste les invitations d'un utilisateur a rejoindre un repertoire
class Invites(tk.Frame):
    labeltextformat = "Invitations ({})"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        self.nbinvitations = 0
        self.label = ttk.Label(self, font = MEDIUMFONT)
        self.updateLabelText()
        self.label.pack(side=LEFT, padx=5, pady=5)
    def callinitrest(self):
        # AVOIR LE NOMBRE D'INVITATION POUR L'UTILISATEUR CONNECTE
        response = requests.get("http://127.0.0.1:5000/users/{}/invites".format(connected_userId)).json()
        self.nbinvitations = 0
        if response["success"]:
            self.nbinvitations = len(json.loads(response["message"]))
            self.updateLabelText()
    def updateLabelText(self):
        self.label.config(text=Invites.labeltextformat.format(self.nbinvitations))
  
# Lancement de l'application
app = tkinterApp()
app.mainloop()
