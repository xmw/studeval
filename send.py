#!/usr/bin/python2
# -*- coding: utf-8 -*-

import mailbox, optparse, smtplib, sys
import email.mime.text, email.parser


parser = optparse.OptionParser()
parser.add_option('-s', '--server', dest='host', default='huygens.fs.lmu.de',
    help='smtp relay server hostname', metavar='STRING')
parser.add_option('-p', '--port', dest='port', default='465',
    help='smtp relay port', 	metavar='STRING')
parser.add_option('-t', '--type', dest='type', default='ssl',
    help='smtp connection type', metavar='plain|ssl|tls')
parser.add_option('-U', '--username', dest='username', default='webermi',
    help='optional smtp username', metavar='STRING')
parser.add_option('-P', '--password', dest='password',
    help='optional smtp password, leave blank for prompt', metavar='STRING')
parser.add_option('-m', '--maildir', dest='maildir', default='mail',
    help='mailbox directory', metavar='DIR')

(options, args) = parser.parse_args()

if not options.host or not options.maildir or not options.type in ('plain', 'ssl', 'tls'):
    parser.print_help()
    sys.exit(1)

if options.username and not options.password:
    import getpass
    options.password = getpass.getpass('Enter password for %s on %s: ' % (options.username, options.host))

mbox = mailbox.Maildir(options.maildir)
mbox.lock()

if options.type == 'ssl':
    conn = smtplib.SMTP_SSL(options.host, int(options.port))
else:
    conn = smtplib.SMTP(options.host, int(options.port))

if options.type == 'tls':
    conn.starttls()

if options.username:
    conn.login(options.username, options.password)

for key in mbox.keys():
    fp = mbox.get_file(key)
    mail = email.parser.Parser().parsestr(fp.read())
    fp.close()
    conn.sendmail(mail.get('From'), mail.get('Rcpt-To'), mail.as_string())
    print mail.get('Rcpt-To')
    mbox.remove(key)
    mbox.flush()

mbox.unlock()
conn.quit()

