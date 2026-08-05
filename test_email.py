import urllib.request
import json
import urllib.error

url = 'http://localhost:8000/api/auth/request-forgot-password'
data = json.dumps({"email": "kaka.babawasim12345@gmail.com"}).encode('utf-8')
req = urllib.request.Request(url, method='POST', headers={'Content-Type': 'application/json'}, data=data)

try:
    res = urllib.request.urlopen(req)
    print("SUCCESS:", res.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR", e.code, e.read().decode())
except Exception as e:
    print('ERROR:', str(e))
