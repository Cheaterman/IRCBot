#!/usr/bin/python
# coding: utf-8

import os, re, sys, time
from datetime import datetime
from pytz import timezone

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime('[{}]'.format(DATE_FORMAT))
        with open(self.file, 'a') as file:
            file.write('%s %s\n' % (timestamp, message))


class IRCBot(irc.IRCClient):
    nickname = 'Weedykins'
    password = ''

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        self.logger = MessageLogger(os.path.join(self.factory.path, 'irc.log'))
        self.logger.log(
            "[Connected to {}]".format(self.factory.hostname)
        )

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log(
            "[Disconnected from {}]".format(self.factory.hostname)
        )

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.logger.log("[Joined {}]".format(self.factory.channel))

    def privmsg(self, prefix, channel, msg):
        user = prefix.split('!')[0]
        self.logger.log("<%s> %s" % (user, msg))

        if(
            msg.startswith('!botsnack') or
            (
                msg.startswith(self.nickname) and
                'botsnack' in msg.lower()
            )
        ):
            msg = "Thanks! Nomnomnom :3"
            self.say(channel, msg, user)

        match = re.match('!seen (\w+)', msg)
        if match:
            nick = match.group(1)
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

        if msg.startswith('!fortune'):
            fortune = os.popen('/usr/games/fortune').read()
            msg = "Fortune: \n{}".format(fortune)
            self.msg(channel, msg)
            for line in msg.split('\n'):
                if line:
                    self.logger.log("<%s> %s" % (self.nickname, line))

        match = re.match('!time ((?:[\w/]+\s*)+)', msg)
        if match:
            argv = match.group(1).split()

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
                self.get_time(channel, of=argv[0], to=user)
        elif msg.startswith('!time'):
            self.get_time(channel, user)

        if 'doobie doobie doo' in msg.lower():
            url = 'https://youtu.be/j4XhDpSgHrs'
            msg = "{} owiiiiii! ^__^".format(url)
            self.say(channel, msg, user)

        match = re.match('!toke(?:\s+(\w+))?', msg)
        if match:
            to = match.group(1)
            msg = "Puff! Puff! Pass{}! ^__^".format(' to {}'.format(to) if to else '')
            self.say(channel, msg, user)

        match = re.match('!join ([^ ]+)', msg)
        if user == 'Cheaterman' and match:
            self.join(match.group(1))

        match = re.match('!part ([^ ]+)', msg)
        if user == 'Cheaterman' and match:
            self.leave(match.group(1))

    def get_time(self, channel, of, to=None):
        if not to:
            to = of

        with open(os.path.join(self.factory.path, 'timezones.yml')) as f:
            for line in f.readlines():
                if line.startswith(of + ':'):
                    nick, timezone_name = line.split(': ')
                    date = datetime.now(timezone(timezone_name[:-1]))
                    msg = "It is currently {}{}".format(
                        date.strftime('%H:%M:%S'),
                        " where {} lives".format(of) if of != to else ''
                    )
                    return self.say(channel, msg, to)

            if to == of:
                msg = "Sorry, I don't know where you live :-$ (set your timezone with !time set <timezone>)"
            else:
                msg = "Sorry, I don't know where {} lives :-$".format(of)
            self.say(channel, msg, to)

    def say(self, channel, msg, to=None):
        if to:
            msg = "{}: {}".format(to, msg)
        self.msg(channel, msg)
        self.logger.log("<{}> {}".format(self.nickname, msg))

    def action(self, prefix, channel, msg):
        user = prefix.split('!')[0]
        self.logger.log("* {} {}".format(user, msg))

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("{} is now known as {}".format(old_nick, new_nick))

    def irc_JOIN(self, prefix, params):
        nick = prefix.split('!')[0]
        self.logger.log("{} joined channel".format(nick))

    def irc_PART(self, prefix, params):
        nick = prefix.split('!')[0]
        channel = params[0]
        self.logger.log("{} left channel {}".format(nick, channel))

    def irc_QUIT(self, prefix, params):
        nick = prefix.split('!')[0]
        reason = params[0]
        self.logger.log("{} quit ({})".format(nick, reason))


class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot

    def __init__(self, hostname, port, channel, path):
        self.hostname = hostname
        self.port = port
        self.channel = channel
        self.path = path

    def clientConnectionLost(self, connector, reason):
        print "Connection lost: {}".format(reason)
        print "Reconnecting..."
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: {}".format(reason)
        reactor.stop()


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = IRCBotFactory(*sys.argv[1:])

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    reactor.connectTCP(hostname, port, factory)

    reactor.run()
