#!/usr/bin/python2
# -*- coding: utf-8 -*-

import email.header, email.mime.text
import optparse, sys, time

SUBJECT="""Studienbeitragssitzung/Evaluationsumfage an der Fakultät 16"""
BODY="""
Sehr geehrte Mitglieder der Studienbeitragskommission,

im Rahmen der Evaluation (TOP 10 Sitzung vom 6.12.2010) haben wir nun den 
Fragebogen fertig und möchten ihn zur Kenntnisnahme vorlegen. 
Dabei erhalten sie unten denselben Text wie er für das spätere Mailing
vorgesehen ist mit einem persönlichen Passwort.

Ich bitte Sie, sich damit vertraut zu machen und etwaige Kritikpunkte auch
an studeval@fs.lmu.de zu schicken um diese Umfrage in der Sitzung vom 6.12.
auf den Weg zu bringen.

i.A. Michael Weber

--

Kommission zur Evaluierung der Studiengebühren an der Fak16

=====================

Liebe Studierende,

inzwischen werden seit fünf Jahren Studienbeiträge erhoben. Seitdem versuchen 
Studierende und Lehrende gemeinsam die Mittel in eurem Sinn einzusetzen. 
Um die Situation weiterhin zu verbessern sind wir auf deine Rückmeldung 
angewiesen und bitten dich bis zum 10. Jannuar 2010 an unserer Umfrage 
unter %s teilzunehmen.

Es gibt zunächst einige allgemeine Fragen, dann spezifische Fragen zu den einzelnen
Instituten Mathe, Informatik und Statistik. Wir bitten dich Angaben zu dem Institut
zu machen, an welchem du dein Hauptfach studierst (z.B. Bioinformatik -> Institut für Informatik).
Verwende dabei den Benutzernamen %s und das Passwort %s.

Die Erhebung der Daten erfolgt anonymisiert. 

Sollte aufgrund kleiner Bildschirmgröße ein Scrollen von links nach rechts auftauchen, 
verkleinere die Anzeige (in den meisten Fällen über die Tastenkombination strg & -).

Vielen Dank für die Teilnahme!

Prof. Heinrich Hussmann,
Dekan der Fakultät für Mathematik, Informatik und Statistik

"""
FROM=email.utils.formataddr((
	str(email.header.Header('Fakultät für Mathematik, Informatik und Statistik', 'utf-8')),
	 'studeval@fs.lmu.de'))
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


