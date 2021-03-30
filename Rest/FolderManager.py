import os
import flask
from flask import Flask, flash, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../Database/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/newfile', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return False
    file = request.files['file']
    if file.filename == '':
        return False
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True

app.run(host="127.0.0.1", port=5000, debug=True)