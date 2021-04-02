import os
import flask
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import json
import uuid
from Utils import Error, Success
import InviteUtils

UPLOAD_FOLDER = './Database/Files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DATABASE_FILE = 'Database/db.json'

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Obtient la liste des repertoires de l'utilisateur connecte    
@app.route('/folders', methods=['GET'])
def getFolders():
    userId = "1"
    db = InviteUtils.loadJson()
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
    folders = db["folder"]
    # Obtention des infos
    body = request.json
    userId = "1"
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
    db = InviteUtils.loadJson()
    folders = db["folder"]
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    return json.dumps(folder, indent = 4)

# Telecharge le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['GET'])
def getFile(folderId, fileId):
    return Success("TODO")

# Upload le fichier
@app.route('/folders/<folderId>/newfile', methods=['POST'])
def upload_file(folderId):
    if 'file' not in request.files:
        return Error("Aucun fichier sélectionné")
    file = request.files['file']
    if file.filename == '':
        return Error("Aucun fichier sélectionné")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Ajout dans la BD
        with open(DATABASE_FILE) as databaseFile:
            db = json.load(databaseFile)
        folders = db['folder']
        for folder in folders:
            if str(folder['id']) == folderId:
                fileEntry = {
                    "id": str(uuid.uuid1()),
                    "name": filename,
                    "type": "XXX",
                    "size": "XXX",
                }
                folder["files"].append(fileEntry)

        json_object = json.dumps(db, indent = 4)
        with open(DATABASE_FILE, 'w') as outfile:
            outfile.write(json_object)

        # Sauvegarde du fichier
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return Success("Le fichier a été téléversé")

# Telecharge le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['PUT'])
def replaceFile(folderId, fileId):
    return Success("TODO")

# Supprime le fichier dont l'id est passe en parametre
@app.route('/folders/<folderId>/<fileId>', methods=['DELETE'])
def deleteFile(folderId, fileId):
    return Success("TODO")

# Change l'administrateur d'un repertoire
@app.route('/folders/<folderId>/admin', methods=['POST'])
def changeAdmin(folderId):
    # Chargement de la BD
    db = InviteUtils.loadJson()
    folders = db["folder"]
    folder = next(filter(lambda f: f["id"] == folderId, folders), None)
    # Obtention des infos
    body = request.json
    userId = "1"
    newAdminUserId = body["userId"]
    if folder["administrator"] is not userId:
        return Error("Seul l'administrateur peut modifier l'administrateur")
    if not newAdminUserId:
        return Error("L'id du nouvel admin est requis")
    # Remplacement de l'admin
    folder["administrator"] = newAdminUserId    
    # Sauvegarde de la BD
    InviteUtils.unloadJson(db)
    # Reponse a l'utilisateur
    return Success("L'administrateur a ete modifie")



#####
## D PARTIE INVITES
#####
# INVITER UN CLIENT <userid> AU REPERTOIRE <folderId>
@app.route("/folders/<folderId>/clients", methods=["POST"])
def sendInvite(folderId):    
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    clientId = request.json["clientId"]

    folderId = int(folderId)
    clientId = int(clientId)
    
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

    #4 - ECRIRE DANS "INVITEDCLIENTS" SI PAS DEJA PRESENT
    if not clientId in folders[findex]["invitedClients"]:
        folders[findex]["invitedClients"].append(clientId)

    InviteUtils.unloadJson(jsondata)

    return Success("")
#####
## F PARTIE INVITES
#####


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
