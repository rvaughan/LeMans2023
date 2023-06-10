import json
import time

import requests


def getMs() -> int:
    return int(round(time.time() * 1000))


check_url = 'https://streaming.24h-lemans.com/en/check?m=0&t=0'
base_url = 'https://storage.googleapis.com/fiawec-prod/assets/live/WEC/__data.json'



def getUrl(url: str) -> str:
    return '{}?_t={}'.format(url, getMs())


def grab_url(url, filename):
    data = requests.get(url)
    if data.status_code == 200:
        with open(f'{filename}.json', 'w') as f:
            json.dump(data.json(), f)


ms=getMs()
filename = f'{ms}_check'
data = requests.get(getUrl(check_url))
if data.status_code == 200:
    with open('{}.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)

check = data.json()
grab_url(check['configuration_url'], f'{ms}_config')
grab_url(check['referential_url'], f'{ms}_reference')
grab_url(check['result_url'], f'{ms}_result')


filename = '{}'.format(getMs())
data = requests.get(getUrl(base_url))
if data.status_code == 200:
    with open('{}.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)

url = 'https://storage.googleapis.com/ecm-prod/assets/live/4793.json?t={}'.format(filename)
data = requests.get(url)
if data.status_code == 200:
    with open('{}_status.json'.format(filename), 'w') as f:
        json.dump(data.json(), f)
