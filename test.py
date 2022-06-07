

import requests
payload = {'api_key': '', 'url':'https://www.google.com/search?client=firefox-b-d&q=gekko+codes', 'autoparse': 'true'}
r = requests.get('http://api.scraperapi.com', params=payload)
print(r.text)
