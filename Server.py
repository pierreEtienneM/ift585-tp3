import socket
import sys
import json
import threading
import time
file = "Database/db.json"

ip = "127.0.0.1"
port = 3839

lastTime = 0
connectedUserList = []
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
s.bind((ip, port))

def printFullUserList():
    with open(file) as f:
        data = json.load(f)

    for user in data['user']:
        print(user['name'])

def validateLogin(username,password):
    with open(file) as f:
        data = json.load(f)

    for user in data['user']:
        if user['name'] == username and user['password'] == password:
            if user['id'] in connectedUserList:
                return (False, "User connected already")
            connectedUserList.append(user['id'])
            return (True, str(user['id']))
    return (False, "Wrong username or password")

def disconnectAllUser():
    with open(file) as f:
        data = json.load(f)

    for user in data['user']:
        user['connectionToken'] = 0

        with open(file,'w') as f:
            json.dump(data,f, indent=4)

def updateToken():
    threading.Timer(5.0, updateToken).start()
    lastTime = int(time.time())

    with open(file) as f:
        data = json.load(f)
    
    print("\n----- Connected Users -----")
    for user in data['user']:
        if user['id'] in connectedUserList and user["connectionToken"] != -1:
            user['connectionToken'] = lastTime  
            print(user['name'])

            with open(file,'w') as f:
                json.dump(data,f, indent=4)
        elif user["connectionToken"] == -1:
            if user['id'] in connectedUserList:
                connectedUserList.remove(user['id'])
            user['connectionToken'] = 0  

            with open(file,'w') as f:
                json.dump(data,f, indent=4)

disconnectAllUser()
print("\n----- Full User List -----")
printFullUserList()
updateToken()
while True:
    print("*** Listenning ***")
    username, address = s.recvfrom(1024)
    password, address = s.recvfrom(1024)
    print("new client trying to connect")
    (success, response) = validateLogin(username.decode("utf-8"),password.decode("utf-8"))

    if success == True:
        print("Connected user from address {0}".format(address))
        s.sendto(str(success).encode('utf-8'), address)
        s.sendto(username, address)
        s.sendto(response.encode('utf-8'), address)
    else:
        s.sendto(bytes(success), address)
        s.sendto(response.encode('utf-8'), address)

#s.close()