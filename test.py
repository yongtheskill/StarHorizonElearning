import requests
url = "https://lv.shel.ml/"

x = requests.get(url, timeout=4)
print(x.status_code)