#!/usr/bin/python2

import re

TOKENFILE = 'studeval.tokens'
TOKENRE = re.compile('Login: ([^ ]*) \| Passwort: ([^ ]*)\n(.*) \n', re.M)

class Token:
    def __init__(self, s):
	self.login, self.password, self.url = TOKENRE.match(s).groups()

    def __str__(self):
	return ' '.join((self.login, self.password, self.url))

def parse(fn = TOKENFILE):
    f = open(fn, 'r')
    data = f.read()
    f.close()
    raw = filter(None, re.split('-----------------------------------------\n', data))
    return map(Token, raw)

if __name__ == '__main__':
    print map(str, parse())
