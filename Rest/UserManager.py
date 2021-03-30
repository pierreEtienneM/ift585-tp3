import flask
import json
from Utils import Error, Success

file = "Database/db.json"
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#serait mieux de caller server.py une méthode disconnectUser(userId) et enlever de la liste au lieu de faire ça.. mais des call de directory parent en python est de la marde..
@app.route('/user/<userId>/disconnect', methods=['POST'])
def userDisconect(userId):
    with open(file) as f:
        data = json.load(f)
        
        for user in data['user']:
            if int(user['id']) == int(userId):
                user['connectionToken'] = -1

    with open(file,'w') as f:
        json.dump(data,f, indent=4)
    
    return Success("Le client est déconnecté")

app.run(host="127.0.0.1", port=5000, debug=True)