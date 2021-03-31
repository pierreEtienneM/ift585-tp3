import tkinter as tk
import requests as r

window = tk.Tk()

#def xCallback():

ADDRESS = "http://127.0.0.1:5000/{}"

def sendInviteCallback(clientid, folderid):
    print("sendInviteCallback")
    url = ADDRESS.format("folders/{}/clients".format(folderid.get()))
    data = {'clientId': int(clientid.get())}
    result = r.post(url = url, json = data)
    print(result.json()["message"])

def getInvitesCallback(folderid):
    print("getInvitesCallback")

def replyInviteCallback(clientid, folderid):
    print("getInvitesCallback")

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)

clientid = tk.IntVar()
folderid = tk.IntVar()

buttons = [0]*3
buttons[0] = ["Send Invite", lambda : sendInviteCallback(clientid, folderid)]
buttons[1] = ["Get Invites", lambda : getInvitesCallback(clientid)]
buttons[2] = ["Reply Invite", lambda : replyInviteCallback(clientid, folderid)]

tk.Label(frame1,text="Client Id").pack(side=tk.LEFT)
tk.Label(frame2,text="Folder Id").pack(side=tk.LEFT)

tk.Entry(frame1,textvariable=clientid).pack(side=tk.RIGHT)
tk.Entry(frame2,textvariable=folderid).pack(side=tk.RIGHT)

for x in buttons:
    tk.Button(frame3,text=x[0], command=x[1]).pack()

frame1.pack()
frame2.pack()
frame3.pack()

window.mainloop()