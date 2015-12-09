import os
from datetime import datetime
from pytz import timezone

from ircbot import bot


@bot.command('!time(?:\s+((?:[\w/]+\s*)+))?')
def time(self, channel, user, argv=None):
    if not argv:
        return get_time(self, channel, user)

    argv = argv.split()

    if argv[0] == 'set':
        if len(argv) != 2:
            msg = "Usage: !time set <timezone> (example: America/Montreal)".format(user)
            return self.say(channel, msg, user)

        try:
            tz = timezone(argv[1])
        except:
            msg = "Sorry, I don't know timezone {}! :-$".format(argv[1])
            return self.say(channel, msg, user)

        with open(os.path.join(self.factory.path, 'timezones.yml'), 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if not line.startswith(user + ':'):
                    f.write(line)
            f.write("{}: {}\n".format(user, argv[1]))
            f.truncate()

        msg = "I successfully saved your timezone {}! ^__^".format(argv[1])
        self.say(channel, msg, user)
    else:
        get_time(self, channel, of=argv[0], to=user)

def get_time(self, channel, of, to=None):
    if not to:
        to = of

    with open(os.path.join(self.factory.path, 'timezones.yml')) as f:
        for line in f.readlines():
            if line.startswith(of + ':'):
                nick, timezone_name = line.split(': ')
                date = datetime.now(timezone(timezone_name[:-1]))
                msg = "It is currently {}{}".format(
                    date.strftime('%H:%M:%S on %d-%m-%Y'),
                    " where {} lives".format(of) if of != to else ''
                )
                return self.say(channel, msg, to)

        if to == of:
            msg = "Sorry, I don't know where you live :-$ (set your timezone with !time set <timezone>)"
        else:
            msg = "Sorry, I don't know where {} lives :-$".format(of)
        self.say(channel, msg, to)
