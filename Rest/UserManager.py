import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/test', methods=['GET'])
def test():
    stringTest = {
    "id": "1", 
    "name": "Bob"
    }
    return stringTest


#####
## D PARTIE INVITES
#####
# AVOIR LES INVITATIONS POUR LE CLIENT <userId>
@app.route("/users/<userId>/invites", methods=["GET"])
def getInvites(userId):
    print("getInvites", request)

# DONNER UNE REPONSE POUR LACCES DU REPERTOIRE <folderId> PAR LE CLIENT <userId>
@app.route("/users/<userId>/invites/<folderId>", methods=["POST"])
def replyInvite(userId, folderId):
    print("replyInvite", request)
#####
## F PARTIE INVITES
#####

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)