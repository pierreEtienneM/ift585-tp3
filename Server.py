import socket
import sys
import json
from Interface.Main import mainPage

file = "Database/db.json"

ip = "127.0.0.1"
port = 3839

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
s.bind((ip, port))

def validateLogin(username,password):
    with open(file) as f:
        data = json.load(f)

    for user in data['user']:
        print(username)
        print(user['password'] == password)
        if user['name'] == username and user['password'] == password:
            print("on login")
            #on cree maybe la clé d'authentification..
            #on redirige l'interface vers la page d'accueil
            return (True, user['id'])
    return False

while True:
    print("*** Listenning ***")
    username, address = s.recvfrom(1024)
    password, address = s.recvfrom(1024)
    print("new client trying to connect")
    (success, userId) = validateLogin(username.decode("utf-8"),password.decode("utf-8"))

    successMessage = "Failure"
    if success == True:
        successMessage = "Success"
        print(address)
        s.sendto(successMessage.encode('utf-8'), address)
        mainPage(username.decode("utf-8"), userId)

    s.sendto(successMessage.encode('utf-8'), address)
s.close()

