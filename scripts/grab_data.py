import json
import time

import requests

# # FP4
# SESSION_ID='4792'
# FIA_ID='2455'

# # Warm Up
# SESSION_ID='4793'
# FIA_ID='2460'

# Race
SESSION_ID='4794'
FIA_ID='2461'


def getMs() -> int:
    return int(round(time.time() * 1000))


base_url = 'https://storage.googleapis.com/fiawec-prod/assets/live/WEC/__data.json'


def getUrl(url: str) -> str:
    return '{}?_t={}'.format(url, getMs())


def grab_url(url, filename):
    data = requests.get(url)
    if data.status_code == 200:
        with open(f'{filename}.json', 'w') as f:
            json.dump(data.json(), f)


ms=getMs()

grab_url(f'https://data.fiawec.com/data/{FIA_ID}', f'{ms}_remaining')
grab_url(f'https://data.fiawec.com/stints/{FIA_ID}', f'{ms}_stints')
grab_url(f'https://data.fiawec.com/laps/{FIA_ID}', f'{ms}_laps')


filename = '{}'.format(getMs())
data = requests.get(getUrl(base_url))
if data.status_code == 200:
    with open('{}.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)

url = f'https://storage.googleapis.com/ecm-prod/assets/live/sessions/{SESSION_ID}.json?t={filename}'
data = requests.get(url)
if data.status_code == 200:
    with open('{}_session.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)

url = f'https://storage.googleapis.com/ecm-prod/assets/live/{SESSION_ID}.json?t={filename}'
data = requests.get(url)
if data.status_code == 200:
    with open('{}_status.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)
