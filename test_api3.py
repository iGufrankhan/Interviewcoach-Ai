import urllib.request, urllib.error
try:
  req = urllib.request.Request('https://interviewcoach-ai-backend.onrender.com//api/auth/send-otp', method='POST', headers={'Content-Type': 'application/json'}, data=b'{"email": "test@example.com"}')
  resp = urllib.request.urlopen(req)
  print(resp.read())
except urllib.error.HTTPError as e:
  print('Error:', e.code, e.read())
