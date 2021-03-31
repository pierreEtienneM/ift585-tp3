import tkinter as tk
import requests as r
import json

window = tk.Tk()

#def xCallback():

ADDRESS = "http://127.0.0.1:5000/{}"

def sendInviteCallback(clientid, folderid):
    print("sendInviteCallback")
    url = ADDRESS.format("folders/{}/clients".format(folderid.get()))
    data = {'clientId': int(clientid.get())}
    result = r.post(url = url, json = data)
    print(result.json()["message"])

def getInvitesCallback(clientid):
    print("getInvitesCallback")
    url = ADDRESS.format("users/{}/invites".format(clientid.get()))
    result = r.get(url = url).json()
    if result["success"]:
        print(json.loads(result["message"]))
    else:
        print(result["message"])

def replyInviteCallback(clientid, folderid, answer):
    print("replyInviteCallback")
    url = ADDRESS.format("users/{}/invites/{}".format(clientid.get(), folderid.get()))
    data = {'answer': int(answer.get())}
    result = r.post(url = url, json = data)
    print(result.json()["message"])

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)
frame4 = tk.Frame(window)

clientid = tk.IntVar()
folderid = tk.IntVar()
answrnum = tk.IntVar()

buttons = [0]*3
buttons[0] = ["Send Invite", lambda : sendInviteCallback(clientid, folderid)]
buttons[1] = ["Get Invites", lambda : getInvitesCallback(clientid)]
buttons[2] = ["Reply Invite", lambda : replyInviteCallback(clientid, folderid, answrnum)]

tk.Label(frame1,text="Client Id").pack(side=tk.LEFT)
tk.Label(frame2,text="Folder Id").pack(side=tk.LEFT)

tk.Entry(frame1,textvariable=clientid).pack(side=tk.RIGHT)
tk.Entry(frame2,textvariable=folderid).pack(side=tk.RIGHT)

tk.Checkbutton(frame4,text="Positive",variable=answrnum,onvalue=1,offvalue=0).pack()

for x in buttons:
    tk.Button(frame3,text=x[0], command=x[1]).pack()

frame1.pack()
frame2.pack()
frame4.pack()
frame3.pack()

window.mainloop()