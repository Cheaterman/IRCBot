from ircbot import bot


@bot.command('blibli (\w+)')
def blibli(self, channel, user, word):
    self.say(channel, 'owiii {}'.format(word))
