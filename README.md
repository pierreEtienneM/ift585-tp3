## Python version 3.9 utilisé, mais python 3+ devrait fonctionner

## Module à installer:
```bash
pip install requests
pip install flask
```

Il faut installer `tk`: `apt install python3-tkinter`

Si `pip` n'est pas disponible : `apt install python3-pip`. Si `pip` ne fonctionne toujours pas, utiliser `pip3`

## Étapes pour fonctionnement de l'application:
1. Lancer le script "startRestAndServer" (regarder Database/db.json pour les users existant)
2. Lancer le script "startClient"
3. Pour l'instant multiple client sur le serveur ne fonctionne pas, mais on va pouvoir lancer plusieurs startClient dans le futur.
