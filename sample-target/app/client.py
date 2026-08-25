import ssl
import urllib.request

import requests


def fetch_partner_data(url):
    response = requests.get(url, verify=False, timeout=10)
    return response.json()


def fetch_legacy_feed(url):
    context = ssl._create_unverified_context()
    return urllib.request.urlopen(url, context=context).read()
