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
