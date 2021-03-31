import json

DATABASE_FILE = "Database/db.json"

def loadJson():
    jsondata = None
    with open(DATABASE_FILE, "r") as dataFile:
        jsondata = json.load(dataFile)
    return jsondata

def unloadJson(jsondata):
    with open(DATABASE_FILE, "w") as dataFile:
        dataFile.write(json.dumps(jsondata, indent = 4))

def _isFolderExists(json, folderId):
    for index, folder in enumerate(json["folder"]):
        if int(folderId) == int(folder["id"]):
            return (True, index)
    return (False, 0)

def _isUserExists(json, clientId):
    for index, user in enumerate(json["user"]):
        if int(clientId) == int(user["id"]):
            return (True, index)
    return (False, 0)

def isExists(json, id, type):
    if type == "FOLDER":
        return _isFolderExists(json, id)
    elif type == "USER":
        return _isUserExists(json, id)
    return (False, 0)