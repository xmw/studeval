#!/usr/bin/python2
# -*- coding: utf-8 -*-

import email.header, email.mime.text
import optparse, sys, time

SUBJECT="""Evaluierung der Vergabe der Studiengebühren an der Fakultät 16"""
BODY="""Liebe Testteilnehmer,

Bitte gehe auf die Seite %s und 
trage Benutzernamen %s und Passwort %s ein.

Vielen Dank für die Teilnahme

Michael Weber
"""
FROM=email.utils.formataddr(('Michael Weber', 'studeval-pretest@fs.lmu.de'))
DATE=email.utils.formatdate(time.time(), True, True)

def generate(rcpt, token):
	msg = email.mime.text.MIMEText(BODY % (token.url, token.login, token.password), 'plain', 'utf-8')
	msg['Subject'] = email.header.Header('Evaluierung der Vergabe der Studiengebühren an der Fakultät 16', 'utf-8')
	msg['From'] = FROM
	msg['Rcpt-To'] = rcpt
	msg['Date'] = DATE
	return msg.as_string()


parser = optparse.OptionParser()
parser.add_option('-a', '--addresses', dest='addrfile',
    help='one email address per line', metavar='FILE')
parser.add_option('-t', '--tokens', dest='tokenfile',
    help='token file', metavar='FILE')
parser.add_option('-s', '--tokenstart', dest='tokenstart',
    help='token number to start', metavar='NUMBER', default='19800')
parser.add_option('-m', '--maildir', dest='maildir',
    help='mailbox directory', metavar='DIR', default='mail')

(options, args) = parser.parse_args()

if not options.addrfile or not options.tokenfile or not options.maildir:
    parser.print_help()
    sys.exit(1)

import mailbox
import token

tokens = token.parse(options.tokenfile)[int(options.tokenstart):][::-1]

mbox = mailbox.Maildir(options.maildir)
mbox.lock()

for line in filter(None, map(lambda s: s.strip(), open(options.addrfile).readlines())):
    print line
    mbox.add(generate(line.strip(), tokens.pop()))

mbox.unlock()
mbox.close()


