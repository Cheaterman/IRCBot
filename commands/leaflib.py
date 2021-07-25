import json
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


LEAFLY_URI = 'https://www.leafly.com'


@dataclass
class Strain:
    name: str
    description: str


def search(strain_name):
    response = requests.get(f'{LEAFLY_URI}/search?q={strain_name}')
    soup = BeautifulSoup(response.text, 'html.parser')
    strains_data = json.loads(soup.find(id='__NEXT_DATA__').string)[
        'props'
    ]['initialState']['search']['strain']

    return [
        Strain(
            name=data['name'],
            description=data['shortDescriptionPlain'],
        )
        for data in strains_data
    ]
