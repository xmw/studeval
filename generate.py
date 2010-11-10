#!/usr/bin/python2
# -*- coding: utf-8 -*-

import email.header, email.mime.text
import optparse, sys, time

SUBJECT="""Pretest: Evaluierung der Studienbeiträge im Wintersemester 2010/2011 an der Fakultät 16"""
BODY="""
=====================
PRETEST

Dies ist ein Testlauf für die kommende Befragung. 
Bitte nimm dir kurz Zeit den Fragebogen anzuschauen und ggf. auftretende Probleme zu melden.
Bitte bereichere Deine Rückmeldung an studeval-pretest@fs.lmu.de um folgende Daten

Name/Email:

Betriebssystem:

Browser/Version:

Fehler:

Beahte bitte, dass deine Angaben -- aufgrund der kleinen Testgruppe -- im Gegensatz zur 
endgültigen Umfrage nicht anonym sind.

i.A. Michael Weber

--

Kommission zur Evaluierung der Studiengebühren an der Fak16

=====================

Liebe Studentin, lieber Student,

wir, die Kommission zur Evaluierung der Studienbeiträge an der Fakultät 16 - bestenend
aus Studenten und Lehrenden, möchten wissen was Du über die Verwendung deiner Beiträge denkst.

Wir bitten dich daher auf der Seite %s deine Meinung auszudrücken. 
Verende dabei den Benutzernamen %s und das Passwort %s.

Die erhebung der Daten erfolgt anonymisiert.

Vielen Dank für die Teilnahme

i. A. Michael Weber

--

Kommission zur Evaluierung der Studiengebühren an der Fak16
email: studeval@fs.lmu.de

"""
FROM=email.utils.formataddr(('Studeval Pretest', 'studeval-pretest@fs.lmu.de'))
DATE=email.utils.formatdate(time.time(), True, True)

def generate(rcpt, token):
	msg = email.mime.text.MIMEText(BODY % (token.url, token.login, token.password), 'plain', 'utf-8')
	msg['Subject'] = email.header.Header(SUBJECT, 'utf-8')
	msg['From'] = FROM
	msg['Rcpt-To'] = rcpt
	msg['Date'] = DATE
	return msg.as_string()


parser = optparse.OptionParser()
parser.add_option('-a', '--addresses', dest='addrfile',
    help='one email address per line', metavar='FILE')
parser.add_option('-t', '--tokens', dest='tokenfile', default='tokens',
    help='token file', metavar='FILE')
parser.add_option('-s', '--tokenstart', dest='tokenstart',
    help='token number to start', metavar='NUMBER')
parser.add_option('-m', '--maildir', dest='maildir', default='mail',
    help='mailbox directory', metavar='DIR')

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


