import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import socket
import requests
import json

connected_userId = 0
connected_username = ""
folder_id = None
LARGEFONT =("Verdana", 35)
MEDIUMFONT =("Verdana", 20)
IP = "127.0.0.1"
PORT = 3839
ADDRESS = "http://127.0.0.1:5000"
# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
greetingLabel = None



def showNavigation(frame, controller):
    global greetingLabel

    navigationFrame = tk.Frame(frame)
    navigationFrame.pack(fill="both")    

    def closeProgram():
        requests.post("http://127.0.0.1:5000/user/{0}/disconnect".format(connected_userId))
        controller.destroy()
    def disconnect():
        print(connected_userId)
        requests.post("http://127.0.0.1:5000/user/{0}/disconnect".format(connected_userId))
        controller.show_frame(LoginPage)
        
    homeButton = ttk.Button(navigationFrame, text ="Accueil",
        command = lambda : controller.show_frame(Home))
    homeButton.pack(side=tk.LEFT, padx=5, pady=5)

    disconnectButton = ttk.Button(navigationFrame, text ="Me déconnecter", command = disconnect)
    disconnectButton.pack(side=tk.RIGHT, padx=5, pady=5)

    greetingLabel = ttk.Label(navigationFrame, text="Bonjour {}!".format(connected_username))
    greetingLabel.pack(expand=True, anchor="c")

    controller.protocol("WM_DELETE_WINDOW", closeProgram)
    

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("IFT585Box")
        self.geometry("400x400")

        self.topcontainer = tk.Frame(self, bg="blue")
        showNavigation(self.topcontainer, self)
        self.topcontainer.pack(fill="both", padx=2, pady=2)

        # Creation du conteneur de l'app
        self.maincontainer = tk.Frame(self, bg="red")
        self.maincontainer.pack(fill="both", expand=True, padx=2, pady=2)

        self.maincontainer.grid_rowconfigure(0, weight = 1)
        self.maincontainer.grid_columnconfigure(0, weight = 1)

        # Initialisation du tableau de pages
        self.frames = {}

        # Initialisation des pages de l'application
        for F in (LoginPage, Home, Repositories, Repository, Invites):
            frame = F(self.maincontainer, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        # Affiche la page de login au lancement de l'application
        self.show_frame(LoginPage)
    
    # Affiche la page passee en parametre
    def show_frame(self, cont):
        # Cache la barre d'identification pour la page de login
        if cont is LoginPage:
            self.topcontainer.pack_forget()
        else:
            self.maincontainer.pack_forget()
            greetingLabel.config(text="Bonjour {}!".format(connected_username))
            self.topcontainer.pack(fill="both", padx=2, pady=2)
            self.maincontainer.pack(fill="both", expand=True, padx=2, pady=2)
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

        self.authentificationLabel = ttk.Label(self, text = "")
        self.authentificationLabel.place(x = 130, y = 20)
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
            self.addWrongAuthentification("")

            controller.show_frame(Home)
        else :
            message, address = s.recvfrom(1024)
            self.addWrongAuthentification(message)

    def addWrongAuthentification(self,message):
        self.authentificationLabel.configure(text = message)
  

# Page d'accueil de l'utilisateur connecte
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def repositoriesCommand():
            controller.show_frame(Repositories)

        def invitesCommand():
            controller.show_frame(Invites)

        login_button=tk.Button(self,text='Mes répertoires',command=repositoriesCommand)
        login_button.place(x=100,y=170)

        login_button=tk.Button(self,text='Mes invitations',command=invitesCommand)
        login_button.place(x=190,y=170)


# Page de la liste des repertoires auquel l'utilisateur connecte a acces
class Repositories(tk.Frame):
    buttonFolders = []
    x_pos = 20
    y_pos = 10
    controller_self = None
    canvas = None
    vbar = None

    def __init__(self, parent, controller):
        self.controller_self = controller
        tk.Frame.__init__(self, parent)

        # Affiche la demande de nom du répertoire à créer
        def createFolder():
            nameFolder = simpledialog.askstring(title="", prompt="Nom du répertoire:")
            folder = {
                'name': nameFolder,
            }
            url = ADDRESS + "/folders"
            # TODO : Changer connected_userId par le token
            response = requests.post(url, headers={'Authorization': connected_userId}, json = folder).json()
            message.configure(text = response.get('message'))

        label = tk.Label(self, text = 'Mes répertoires')
        label.pack()
        newDirButton = tk.Button(self, text = 'Créer un répertoire', command = createFolder)
        newDirButton.pack(side = tk.TOP, pady = 5)
        message = tk.Label(self, text="")
        message.pack()

        self.canvas=tk.Canvas(self, scrollregion=(0,0,0,800))
        self.vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(expand=True,fill=tk.BOTH)

        self.after(500, self.refresh)

    # Affiche le frame Repository
    def repositoryCommand(self, id):
        global folder_id
        folder_id = id
        self.controller_self.show_frame(Repository)

    # Supprime les boutons du frame
    def destroyButton(self):
        for button in self.buttonFolders:
            button.destroy()
        self.i = 0
        self.x_pos = 10
        self.y_pos = 10
        self.buttonFolders.clear()

    # Mise à jour de la liste des répertoires
    def refresh(self):
        global connected_userId
        if connected_userId != 0:
            self.destroyButton()
            # Affichage de la liste des répertoires
            # TODO : Changer connected_userId par le token
            list = requests.get(ADDRESS + "/folders", headers={'Authorization': connected_userId}).json()
            for folder in list:
                self.buttonFolders.append(tk.Button(self.canvas, text = folder['name'], width = 20, command = lambda id = folder['id']: self.repositoryCommand(id)))       
            
            j = 1 
            for button in self.buttonFolders:
                self.x_pos = 20
                if j%2 != 0:
                    self.canvas.create_window(self.x_pos, self.y_pos, window=button, anchor=tk.NW)
                    j += 1
                else:
                    self.x_pos = 350
                    self.canvas.create_window(self.x_pos, self.y_pos, window=button, anchor=tk.NE)
                    self.y_pos += 30
                    j -= 1

        # Actualise l'interface des répertoires après 1 seconde
        self.after(1000, self.refresh)


# Page d'un repertoire qui liste les fichiers contenus
class Repository(tk.Frame):
    labelFiles = []
    commandButton = []
    adminButton = []
    canvas = None
    vbar = None
    x_pos = 10
    y_pos = 10
    command_id = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Retourne au frame des répertoires
        def repositoriesCommand():
            controller.show_frame(Repositories)

        # Upload un fichier
        def uploadFile():
            url = ADDRESS + "/folders/" + folder_id + "/newfile"
            f = filedialog.askopenfilename()
            f = open(f, 'rb')
            files = {
                'file': f
            }
            # TODO : Changer connected_userId par le token
            msg = requests.post(url, files=files, headers={'Authorization': connected_userId}).json()
            message.configure(text = msg.get('message'))

        label = tk.Label(self, text = 'Répertoire')
        label.pack()
        message = tk.Label(self, text="")
        message.pack()

        addButton = tk.Button(self, text="Ajouter un fichier", command=uploadFile)
        addButton.place(x=93, y=50)

        retour = tk.Button(self, text="Retour", command=repositoriesCommand)
        retour.place(x=5, y=50, anchor=tk.NW, width=75)

        tk.Label(self, text="Fichier").place(x = 10, y = 90)
        # TODO 
        # À Supprimer ?
        tk.Label(self, text="Type").place(x = 110, y = 90)
        tk.Label(self, text="Taille").place(x = 210, y = 90)
        
        self.canvas=tk.Canvas(self, scrollregion=(0,0,0,800))
        self.vbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vbar.place(x=380, y=120, height=200)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.place(x=0, y=120, height=200)

        self.after(500, self.refresh)

    # Envoie une invitation
    def sendInvite(self):
        url = ADDRESS + "/folders/" + folder_id + "/clients"
        clientId = simpledialog.askstring(title="", prompt="Entrez l'id de l'utilisateur à inviter:")
        if clientId != None:
            body = {
                "clientId" : clientId
            }
            # TODO : Changer connected_userId par le token
            requests.post(url, json=body, headers={'Authorization': connected_userId}).json()
    
    # TODO : Lister les users par leurs id ? Ou choisir dans une liste ?
    # Change l'administrateur du répertoire
    def changeAdmin(self):
        url = ADDRESS + "/folders/" + folder_id + "/admin"
        userId = simpledialog.askstring(title="", prompt="Entrez l'id du nouvel administrateur:")
        if userId != None:
            body = {
                "userId" : str(userId)
            }
            # TODO : Changer connected_userId par le token
            requests.post(url, json=body, headers={'Authorization': connected_userId}).json()

    # Supprime le fichier
    def deleteFile(self, fileId):
        url = ADDRESS + "/folders/" + str(folder_id) + "/" + str(fileId)
        # TODO : Changer connected_userId par le token
        requests.delete(url, headers={'Authorization': connected_userId}).json()
    
    # Télécharge le fichier
    def downloadFile(self, fileId, name):
        url = ADDRESS + "/folders/" + str(folder_id) + "/" + str(fileId)
        # TODO : Changer connected_userId par le token
        file_bin = requests.get(url, headers={'Authorization': connected_userId})
        f = filedialog.asksaveasfilename(initialfile = name, filetypes=[("All files", "*.*")])
        f = open(f, 'wb')
        f.write(file_bin.content)
    
    # Efface les boutons et les labels pour l'actualisation
    def destroyButton(self):
        for labels in self.labelFiles:
            labels.destroy()
        for button in self.commandButton:
            button.destroy()
        for button in self.adminButton:
            button.destroy()
        self.y_pos = 10
        self.command_id = 0
        self.commandButton.clear()
        self.labelFiles.clear()
        self.adminButton.clear()

    # Actualisation de l'interface
    def refresh(self):
        global folder_id

        if folder_id != None and connected_userId != 0:

            # Afficher invitation et changement d'admin
            self.destroyButton()
            response = requests.get(ADDRESS + "/folders/" + str(folder_id) + "/admin", headers={'Authorization': connected_userId})
            administrator = response.content.decode("utf-8")
            if administrator == connected_userId:
                inviteButton = tk.Button(self, text="Invite", command=lambda: self.sendInvite())
                inviteButton.place(x=208, y=50, width=75)
                self.adminButton.append(inviteButton)

                adminButton = tk.Button(self, text="Changer d'admin", command=lambda: self.changeAdmin())
                adminButton.place(x=295, y=50, width=100)
                self.adminButton.append(adminButton)

            # Affichage de la liste des fichiers            
            # TODO : Changer connected_userId par le token
            list = requests.get(ADDRESS + "/folders/" + str(folder_id), headers={'Authorization': connected_userId}).json()
            for files in list['files']:
                name = files['name']

                self.labelFiles.append(tk.Label(self, text = name))

                self.commandButton.append(tk.Button(self.canvas, text = "Télécharger", command = lambda id = files['id']: self.downloadFile(id, name)))
                if administrator == connected_userId:
                    self.commandButton.append(tk.Button(self.canvas, text = "X", bg="#ff4545", fg="white", command = lambda id = files['id']: self.deleteFile(id)))
        
            for labels in self.labelFiles:
                # Affiche le nom du fichier
                self.canvas.create_window(self.x_pos, self.y_pos, window=labels, anchor=tk.NW)

                # Affiche les bouttons télécharger et supprimer
                downloadButton = self.commandButton[self.command_id]
                self.canvas.create_window(self.x_pos + 270, self.y_pos, window=downloadButton, anchor=tk.NW)
                self.command_id += 1
                if administrator == connected_userId:
                    deleteButton = self.commandButton[self.command_id]
                    self.canvas.create_window(self.x_pos + 345, self.y_pos, window=deleteButton, anchor=tk.NW)
                    self.command_id += 1                
                self.y_pos += 30

        # Actualise l'interface après 3 secondes
        self.after(3000, self.refresh)

# Page qui liste les invitations d'un utilisateur a rejoindre un repertoire
class Invites(tk.Frame):
    labelFolders = []
    commandButton = []
    canvas = None
    vbar = None
    x_pos = 10
    y_pos = 10
    command_id = 0
    labeltextformat = "Invitations ({})"
    nbinvitations = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, font = MEDIUMFONT)
        self.updateLabelText()
        self.label.pack()

        tk.Label(self, text="Répertoire").place(x = 10, y = 60)
        self.canvas=tk.Canvas(self, scrollregion=(0,0,0,800))
        self.vbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vbar.place(x=380, y=90, height=230)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.place(x=0, y=90, height=230)

        self.after(500, self.refresh)

    def callinitrest(self):
        # AVOIR LE NOMBRE D'INVITATION POUR L'UTILISATEUR CONNECTE
        response = requests.get("http://127.0.0.1:5000/users/{}/invites".format(connected_userId)).json()
        self.nbinvitations = 0
        for folders in response:
            self.nbinvitations += 1
        self.updateLabelText()
    def updateLabelText(self):
        self.label.config(text=Invites.labeltextformat.format(self.nbinvitations))

    # Reponse à l'invitation
    def replyInvite(self, folderId, answer):
        url = ADDRESS + "/users/" + str(connected_userId) + "/invites/" + folderId
        invite = {
            "answer" : str(answer)
        }
        requests.post(url, json=invite, headers={'Authorization': connected_userId}).json()
        
    # Efface les boutons et les labels pour l'actualisation
    def destroyButton(self):
        for labels in self.labelFolders:
            labels.destroy()
        for button in self.commandButton:
            button.destroy()
        self.y_pos = 10
        self.command_id = 0
        self.commandButton.clear()
        self.labelFolders.clear()

    # Actualisation de l'interface
    def refresh(self):
        if connected_userId != 0:
            # Affichage de la liste des invitations
            self.destroyButton()
            # TODO : Changer connected_userId par le token
            list = requests.get(ADDRESS + "/users/" + connected_userId + "/invites", headers={'Authorization': connected_userId}).json()
            for folders in list:
                
                name = folders['name']

                self.labelFolders.append(tk.Label(self, text = name))

                self.commandButton.append(tk.Button(self.canvas, text = "Accepter", bg="#47d187", fg="white", command = lambda id = folders['id']: self.replyInvite(id, 1)))
                self.commandButton.append(tk.Button(self.canvas, text = "Refuser", bg="#ff4545", fg="white", command = lambda id = folders['id']: self.replyInvite(id, 0)))
        
            for labels in self.labelFolders:
                # Affiche le nom du répertoire
                self.canvas.create_window(self.x_pos, self.y_pos, window=labels, anchor=tk.NW)

                # Affiche les bouttons télécharger et supprimer
                acceptButton = self.commandButton[self.command_id]
                denyButton = self.commandButton[self.command_id+1]
                self.canvas.create_window(self.x_pos + 240, self.y_pos, window=acceptButton, anchor=tk.NW)
                self.canvas.create_window(self.x_pos + 305, self.y_pos, window=denyButton, anchor=tk.NW)
                self.command_id += 2
                self.y_pos += 30                

        # Actualise l'interface après 3 secondes
        self.after(3000, self.refresh)

# Lancement de l'application
app = tkinterApp()
app.mainloop()
