# coding: utf-8

import re
from datetime import datetime

from ircbot import bot
from chatlog import DATE_FORMAT


@bot.command('!seen (\w+)')
def seen(self, channel, user, nick):
    log_regexp = (
        (
            "\[[^\]]+\] <{}> (.*)",
            "{} was last seen {} ago saying « {} »"
        ),
        (
            "\[[^\]]+\] \* {} (.*)",
            "{} was last seen {} ago, « {} »"
        ),
        (
            "\[[^\]]+\] {} is now known as (.*)",
            "{} was last seen {} ago, changing name to « {} »"
        ),
        (
            "\[[^\]]+\] {} joined channel",
            "{} was last seen {} ago, joining channel"
        ),
        (
            "\[[^\]]+\] {} left channel \((.*)\)",
            "{} was last seen {} ago, leaving channel ({})"
        ),
        (
            "\[[^\]]+\] {} quit \((.*)\)",
            "{} was last seen {} ago, quitting ({})"
        ),
    )
    log_regexp = [(re.compile(pattern.format(nick)), msg) for pattern, msg in log_regexp]
    time_regexp = re.compile("\[(\d+/\d+/\d+ \d+:\d+:\d+)\]")

    with open(self.logger.file) as file:
        for line in reversed(list(file)[:-1]):
            time_interval = get_time_interval(line, time_regexp)

            for regexp, msg in log_regexp:
                match = regexp.match(line)
                if match:
                    msg = msg.format(nick, time_interval, *match.groups())
                    return self.say(channel, msg, user)

        msg = "Sorry, I haven't seen {}! :-$".format(nick)
        self.say(channel, msg, user)

def get_time_interval(line, regexp):
    match = regexp.match(line)
    if match:
        date = match.group(1)
        delta = datetime.now() - datetime.strptime(date, DATE_FORMAT)

        years, remainder = divmod(delta.seconds, 3600 * 24 * 365)
        months, remainder = divmod(remainder, 3600 * 24 * 30)
        days, remainder = divmod(remainder, 3600 * 24)
        hours, remainder = divmod(remainder, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds = remainder

        time_interval = '{}{}{}{}{}{}'.format(
            '{} year{}, '.format(years, 's' if years > 1 else '') if years else '',
            '{} month{}, '.format(months, 's' if months > 1 else '') if months else '',
            '{} day{}, '.format(days, 's' if days > 1 else '') if days else '',
            '{} hour{}, '.format(hours, 's' if hours > 1 else '') if hours else '',
            '{} minute{} '.format(minutes, 's' if minutes > 1 else '') if hours or minutes else '',
            '{}{} second{}'.format(
                'and ' if any((years, months, days, hours, minutes)) else '',
                seconds,
                's' if seconds > 1 else ''
            )
        )
    else:
        time_interval = 'a while'

    return time_interval
