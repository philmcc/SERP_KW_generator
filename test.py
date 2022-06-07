

import requests
payload = {'api_key': '0cee3fe13dcac1e1086b04d623a89142', 'url':'https://www.google.com/search?client=firefox-b-d&q=gekko+codes', 'autoparse': 'true'}
r = requests.get('http://api.scraperapi.com', params=payload)
print(r.text)
