import os
import requests
url = "http://localhost/live/cleanupLivestreamServer"

try:
    os.environ['NO_PROXY'] = '127.0.0.1'
    x = requests.get(url, timeout=10)
    print(x.status_code)
    print(x.content)
except Exception as e:
    print("cleanup failed: " + str(e))