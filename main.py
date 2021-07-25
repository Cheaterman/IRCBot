#!/usr/bin/python

import sys

from twisted.internet import reactor, ssl
from twisted.python import log

from ircbot import bot


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    reactor.connectSSL(hostname, port, bot, ssl.ClientContextFactory())

    reactor.run()
