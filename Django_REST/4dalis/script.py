import requests

url = 'http://127.0.0.1:8000/posts/8/like'
headers = {'Authorization': 'Token 761fee26e056d4fc065dc4edf7c2b1b9482d6f40'}
r = requests.post(url, headers=headers)

print(r.json())

# ['Jūs jau palikote patiktuką šiam pranešimui!']