import os
import flask
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import json
import uuid
from Utils import Error, Success

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

app.run(host="127.0.0.1", port=5000, debug=True)