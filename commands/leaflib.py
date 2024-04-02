import json
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


LEAFLY_URI = 'https://consumer-api.leafly.com/api/search/v1'


@dataclass
class Strain:
    name: str
    description: str


def search(strain_name):
    response = requests.get(LEAFLY_URI, params={'q': strain_name})
    strains_data = response.json()['hits']['strain']

    return [
        Strain(
            name=data['name'],
            description=data['shortDescriptionPlain'],
        )
        for data in strains_data
    ]
