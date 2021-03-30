import tkinter as tk
from tkinter import ttk, NE, NW
import socket
import requests
 
LARGEFONT =("Verdana", 35)
MEDIUMFONT =("Verdana", 20)
IP = "127.0.0.1"
PORT = 3839
# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

def showNavigation(frame, controller):
    homeButton = ttk.Button(frame, text ="Accueil",
        command = lambda : controller.show_frame(Home))
    homeButton.grid(row = 0, column=0)

    disconnectButton = ttk.Button(frame, text ="Me déconnecter",
        command = lambda : controller.show_frame(Home))
    disconnectButton.grid(row = 0, column=12)

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
        
        if success.decode("utf-8") == "Success":
            controller.show_frame(Home)
        else :
            self.addWrongAuthentification()

    def addWrongAuthentification(self):
        ttk.Label(self, text = 'Wrong username or password.. Try again' ).place(x=100,y=20)
  

# Page d'accueil de l'utilisateur connecte
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def repositoriesCommand():
            controller.show_frame(Repositories)

        def invitesCommand():
            controller.show_frame(Invites)

        ttk.Label(self, text = 'Bonjour').place(x=170,y=0)

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
        label.grid(row = 1, column = 0, columnspan=12, padx = 10, pady = 10)


# Page d'un repertoire qui liste les fichiers contenus
class Repository(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        label = ttk.Label(self, text ="Répertoire XXX", font = MEDIUMFONT)
        label.grid(row = 1, column = 0, columnspan=12, padx = 10, pady = 10)


# Page qui liste les invitations d'un utilisateur a rejoindre un repertoire
class Invites(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        showNavigation(self, controller)

        label = ttk.Label(self, text ="Invitations", font = MEDIUMFONT)
        label.grid(row = 1, column = 0, columnspan=12, padx = 10, pady = 10)

  
# Lancement de l'application
app = tkinterApp()
app.mainloop()