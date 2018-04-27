from ircbot import bot
import requests


STRAIN_API_URI = 'http://strainapi.evanbusse.com'


@bot.command('!strain (.*)')
def strain(self, channel, user, name):
    response = requests.get(
        STRAIN_API_URI + '/{API_KEY}/strains/search/name/{NAME}'.format(
            API_KEY='WhAdfsc',
            NAME=name,
        )
    )
    data = response.json()

    msg = None

    if data:
        for strain in data:
            if strain['desc']:
                msg = strain['desc'].encode('utf8')
                break

    if not msg:
        msg = 'Sorry, strain "{}" not found :-S'.format(name)

    self.say(channel, msg, user)
