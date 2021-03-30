import tkinter as tk
from tkinter import ttk, Entry
import requests

def invitePage():

    window = tk.Tk()

    window.title("Mes invitations")
    window.geometry("400x400")

    tk.Grid.rowconfigure(window, 0, weight=1)
    tk.Grid.columnconfigure(window, 0, weight=1)

    frame = tk.Frame(window)
    frame.grid(row=0,column=0,sticky="NSEW")

    tk.Grid.rowconfigure(frame, 1, weight=1)
    tk.Grid.columnconfigure(frame, 0, weight=1)
    tk.Grid.columnconfigure(frame, 1, weight=4)
    tk.Grid.columnconfigure(frame, 2, weight=1)

    tk.Button(frame, text="BACK").grid(row=0, column=0, sticky="NSEW")
    tk.Label(frame, text="Mes invitations").grid(row=0, column=1, sticky="NSEW")
    tk.Button(frame, text="LOGOUT").grid(row=0, column=2, sticky="NSEW")

    # FILL INVITATIONS HERE

    window.mainloop()

if __name__ == "__main__":
    invitePage()
    print("OK")
