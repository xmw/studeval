#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re

TOKENFILE = 'tokens'
TOKENRE = re.compile('Login: ([^ ]*) \| Passwort: ([^ ]*)\n(.*) \n', re.M)

class Token:
    def __init__(self, s):
	self.login, self.password, self.url = TOKENRE.match(s).groups()
	self.url = 'http://' + self.url

    def __str__(self):
	return ' '.join((self.login, self.password, self.url))

def parse(fn = TOKENFILE):
    f = open(fn, 'r')
    data = f.read()
    f.close()
    raw = filter(None, re.split('-----------------------------------------\n', data))
    return map(Token, raw)

if __name__ == '__main__':
    for token in parse():
	print token
