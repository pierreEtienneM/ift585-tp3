import requests

url = "http://127.0.0.1:5000/newfile"

files = {
    'file': open('testFile.txt', 'rb') # rb est le mode "read-binary"
}

response = requests.post(url, files=files)

print(response.status_code)
print(response.text)