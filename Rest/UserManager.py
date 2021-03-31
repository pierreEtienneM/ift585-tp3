import flask
import json
from Utils import Error, Success
import InviteUtils

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

#####
## D PARTIE INVITES
#####
# AVOIR LES INVITATIONS POUR LE CLIENT <userId>
@app.route("/users/<userId>/invites", methods=["GET"])
def getInvites(userId):    
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    clientId = int(userId)
    
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

    return Success(json.dumps(invitedFolders, indent = 4))

# DONNER UNE REPONSE POUR LACCES DU REPERTOIRE <folderId> PAR LE CLIENT <userId>
@app.route("/users/<userId>/invites/<folderId>", methods=["POST"])
def replyInvite(userId, folderId):
    print("replyInvite", request)
#####
## F PARTIE INVITES
#####

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)