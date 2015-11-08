# coding: utf-8

import re
from datetime import datetime

from ircbot import bot
from logging import DATE_FORMAT


@bot.command('!seen (\w+)')
def seen(self, channel, user, nick):
    with open(self.logger.file) as file:
        for line in reversed(list(file)[:-1]):
            match = re.match("\[(\d+/\d+/\d+ \d+:\d+:\d+)\]", line)
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

            match = re.match("\[[^\]]+\] <{}> (.*)".format(nick), line)
            if match:
                msg = "{} was last seen {} ago saying « {} »".format(nick, time_interval, match.group(1))
                self.say(channel, msg, user)
                break

            match = re.match("\[[^\]]+\] \* {} (.*)".format(nick), line)
            if match:
                msg = "{} was last seen {} ago, « {} »".format(nick, time_interval, match.group(1))
                self.say(channel, msg, user)
                break

            match = re.match("\[[^\]]+\] {} is now known as (.*)".format(nick), line)
            if match:
                msg = "{} was last seen {} ago, changing name to « {} »".format(nick, time_interval, match.group(1))
                self.say(channel, msg, user)
                break

            match = re.match("\[[^\]]+\] {} joined channel".format(nick), line)
            if match:
                msg = "{} was last seen {} ago, joining channel".format(nick, time_interval)
                self.say(channel, msg, user)
                break

            match = re.match("\[[^\]]+\] {} left channel \((.*)\)".format(nick), line)
            if match:
                msg = "{} was last seen {} ago, leaving channel ({})".format(nick, time_interval, match.group(1))
                self.say(channel, msg, user)
                break

            match = re.match("\[[^\]]+\] {} quit \((.*)\)".format(nick), line)
            if match:
                msg = "{} was last seen {} ago, quitting ({})".format(nick, time_interval, match.group(1))
                self.say(channel, msg, user)
                break

        if not match:
            msg = "Sorry, I haven't seen {}! :-$".format(nick)
            self.say(channel, msg, user)
