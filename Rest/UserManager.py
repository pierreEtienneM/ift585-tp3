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
    # 1 - OUVRIR LA BASE DE DONNEE
    jsondata = InviteUtils.loadJson()
    answer = int(flask.request.json["answer"])

    # 0 : FALSE
    # TRUE

    clientId = int(userId)
    folderId = int(folderId)

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