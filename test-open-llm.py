import requests

resp = requests.post("210.40.16.12:23165", json=[{"role": "user", "content": "TigerBot"}])
print(resp)