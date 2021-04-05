import os
import flask
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import json
import uuid
from Utils import Error, Success
import InviteUtils

UPLOAD_FOLDER = './Database/Files'
DATABASE_FILE = 'Database/db.json'

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

######
##  FolderManager
######

def getUserId(db, request):
    users = db["user"]
    if request.headers.get("Authorization"):
        connectionToken = request.headers["Authorization"]
        # TODO : Garder seulement la ligne avec connectionToken, l'id utilisé seulement pour les tests
        #user = next(filter(lambda u: u["connectionToken"] == connectionToken, users), None)
        user = next(filter(lambda u: u["id"] == connectionToken, users), None)
        if user:
            return user["id"]

# Obtient la liste des repertoires de l'utilisateur connecte    
@app.route('/folders', methods=['GET'])
def getFolders():
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db["folder"]
    userFolders = list(filter(lambda f: userId in f["clients"], folders))
    for folder in userFolders:
        folder.pop("files", None)
    return json.dumps(userFolders, indent = 4)

# Crée un répertoire pour l’utilisateur connecté  
@app.route('/folders', methods=['POST'])
def createFolder():
    # Chargement de la BD
    db = InviteUtils.loadJson()
     # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db["folder"]
    body = request.json
    folderName = body["name"]
    if not folderName:
        return Error("Le nom du dossier est requis")
    # Creation du dossier
    folderId = uuid.uuid4().hex
    newfolder = {
        "id": folderId,
        "name": folderName,
        "files": [],
        "invitedClients": [],
        "clients": [userId],
        "administrator": userId
    }
    folders.append(newfolder)
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return json.dumps(newfolder, indent = 4)

# Affiche le contenu d’un répertoire dans l’application
@app.route('/folders/<folderId>', methods=['GET'])
def getFolder(folderId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db["folder"]
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    return json.dumps(folder, indent = 4)

# Telecharge le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['GET'])
def getFile(folderId, fileId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db['folder']
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    fileEntry = next(filter(lambda f: f["id"] == fileId, folder["files"]), None)
    if not fileEntry:
        return Error("Aucun fichier n'a cet id")
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], fileId), "rb")
    # Reponse a l'utilisateur
    return file.read()

# Retourne l'administrateur d'un repertoire
@app.route('/folders/<folderId>/admin', methods=['GET'])
def getAdmin(folderId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db["folder"]
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    return folder["administrator"]

# Upload le fichier
@app.route('/folders/<folderId>/newfile', methods=['POST'])
def postFile(folderId):
    # Validations
    if 'file' not in request.files:
        return Error("Aucun fichier sélectionné")
    file = request.files['file']
    if file.filename == '':
        return Error("Aucun fichier sélectionné")
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db['folder']
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    filename = secure_filename(file.filename)
    fileId =  uuid.uuid4().hex
    # Sauvegarde du fichier sur le disque
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileId))
    # Creation de l'entree du fichier
    fileEntry = {
        "id": fileId,
        "name": filename,
    }
    folder["files"].append(fileEntry)
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return Success("Le fichier a été téléversé")

# Telecharge le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['PUT'])
def replaceFile(folderId, fileId):
    # Validations
    if 'file' not in request.files:
        return Error("Aucun fichier sélectionné")
    file = request.files['file']
    if file.filename == '':
        return Error("Aucun fichier sélectionné")

    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db['folder']
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    fileEntry = next(filter(lambda f: f["id"] == fileId, folder["files"]), None)
    if not fileEntry:
        return Error("Aucun fichier n'a cet id")
    filename = secure_filename(file.filename)
    # Sauvegarde du fichier sur le disque
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileId))
    # Modification de l'entree du fichier
    fileEntry["name"] = filename
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return Success("Le fichier a été téléversé")

# Supprime le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['DELETE'])
def deleteFile(folderId, fileId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db['folder']
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    fileEntry = next(filter(lambda f: f["id"] == fileId, folder["files"]), None)
    if not fileEntry:
        return Error("Aucun fichier n'a cet id")
    # Suppression de l'entree du fichier dans la BD
    newFilesArray = list(filter(lambda f: f["id"] != fileId, folder["files"]))
    folder["files"] = newFilesArray
    # Suppression du fichier sur le disque
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fileId))
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return Success("Le fichier a été supprimé")

# Change l'administrateur d'un repertoire
@app.route('/folders/<folderId>/admin', methods=['POST'])
def changeAdmin(folderId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    # Authentification
    userId = getUserId(db, request)
    if not userId:
        return Error("Utilisateur n'est pas connecté")
    # Obtention des infos
    folders = db["folder"]
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    body = request.json
    newAdminUserId = body["userId"]
    if folder["administrator"] is not userId:
        return Error("Seul l'administrateur peut modifier l'administrateur")
    if not newAdminUserId:
        return Error("L'id du nouvel admin est requis")
    users = db["user"]
    user = next(filter(lambda u: u["id"] == newAdminUserId, users), None)
    if not user:
        return Error("L'id du nouvel admin n'existe pas")
    # Remplacement de l'admin
    folder["administrator"] = newAdminUserId    
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return Success("L'administrateur a été modifié")



#####
## D PARTIE INVITES
#####
# INVITER UN CLIENT <userid> AU REPERTOIRE <folderId>
@app.route("/folders/<folderId>/clients", methods=["POST"])
def sendInvite(folderId):    
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    clientId = request.json["clientId"]

    folderId = folderId
    clientId = clientId
    
    if jsondata == None:
        return Error("Erreur lors de l'ouverture de la BD.")

    folders = jsondata["folder"]

    # 2 - VERIFIER SI LE DOSSIER EXISTE
    found, findex = InviteUtils.isExists(jsondata, folderId, "FOLDER")
    if not found:
        return Error("Erreur lors de la recherche du repertoire.")

    # 3 - VERIFIER SI LE CLIENT EXISTE
    found, cindex = InviteUtils.isExists(jsondata, clientId, "USER")
    if not found:
        return Error("Erreur lors de la recherche du client.")

    if not clientId in folders[findex]["administrator"]:
        return Error("Erreur le client n'a pas les droits.")

    #4 - ECRIRE DANS "INVITEDCLIENTS" SI PAS DEJA PRESENT
    if not clientId in folders[findex]["invitedClients"]:
        folders[findex]["invitedClients"].append(clientId)

    InviteUtils.unloadJson(jsondata)

    return Success("Invitation envoyée")
#####
## F PARTIE INVITES
#####


######
##  UserManager
######
#serait mieux de caller server.py une méthode disconnectUser(userId) et enlever de la liste au lieu de faire ça.. mais des call de directory parent en python est de la marde..
@app.route('/user/<userId>/disconnect', methods=['POST'])
def userDisconect(userId):
    with open(DATABASE_FILE) as f:
        data = json.load(f)
        
        for user in data['user']:
            if int(user['id']) == int(userId):
                user['connectionToken'] = -1

    with open(DATABASE_FILE,'w') as f:
        json.dump(data,f, indent=4)
    
    return Success("Le client est déconnecté")

#####
## D PARTIE INVITES
#####
# AVOIR LES INVITATIONS POUR LE CLIENT <userId>
@app.route("/users/<userId>/invites", methods=["GET"])
def getInvites(userId):    
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    clientId = userId
    
    if jsondata == None:
        return Error("Erreur lors de l'ouverture de la BD.")

    folders = jsondata["folder"]

    # 2 - VERIFIER SI LE CLIENT EXISTE
    found, cindex = InviteUtils.isExists(jsondata, clientId, "USER")
    if not found:
        return Error("Erreur lors de la recherche du client.")

    invitedFolders = []
    for folder in folders:
        if clientId in folder["invitedClients"]:
            invitedFolders.append(folder)

    return json.dumps(invitedFolders, indent = 4)

# DONNER UNE REPONSE POUR LACCES DU REPERTOIRE <folderId> PAR LE CLIENT <userId>
@app.route("/users/<userId>/invites/<folderId>", methods=["POST"])
def replyInvite(userId, folderId):
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    answer = int(flask.request.json["answer"])

    # 0 : FALSE
    # TRUE

    clientId = userId
    folderId = folderId

    # 2 - VERIFIER SI LE CLIENT EXISTE
    found, cindex = InviteUtils.isExists(jsondata, clientId, "USER")
    if not found:
        return Error("Erreur lors de la recherche du client.")

    # 3 - VERIFIER SI LE DOSSIER EXISTE
    found, findex = InviteUtils.isExists(jsondata, folderId, "FOLDER")
    if not found:
        return Error("Erreur lors de la recherche du repertoire.")

    folder = jsondata["folder"][findex]

    isclient = clientId in folder["clients"]
    isinvite = clientId in folder["invitedClients"]

    # 4 - VERIFIER LES DEMANDES DACCESS
    if not isinvite and not isclient:
        return Error("Le client n'a pas eu l'access au dossier.")
    
    # 5 - AJOUTER L'ACCES
    needwrite = False
    if isinvite:
        folder["invitedClients"].remove(clientId)
        needwrite = True
    
    if answer != 0 and not isclient:
        folder["clients"].append(clientId)
        needwrite = True
    
    if needwrite:
        InviteUtils.unloadJson(jsondata)

    if answer == 0:
        return Success("Acces enleve.")
    return Success("Acces ajoute.")
#####
## F PARTIE INVITES
#####

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
