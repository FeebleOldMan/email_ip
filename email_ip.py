#!/usr/bin/env python3
"""Email IP

Emails IP address of client.

This script is meant to be run on a Raspberry Pi in order to obtain its IP
address via email.

Run this file on startup (i.e. add to /etc/rc.local).
"""

import getopt
import re
import sys
from smtplib import SMTP
from subprocess import Popen, PIPE
from email.mime.text import MIMEText

### CHANGE THE FOLLOWING SETTINGS ###
PI_NAME = 'raspberry pi'
RECIPIENT_EMAIL = 'pi@example.com'
SENDER_GMAIL = 'example@gmail.com'
SENDER_PASSWORD = 'example_password'
#####################################

def get_ip_addresses():
    """Returns list of local IP addresses."""
    raw_ip_list = Popen('ip route list',
                        shell=True,
                        stdout=PIPE,
                        universal_newlines=True
                       ).stdout.read().splitlines()
    ip_src_re = re.compile(r'src (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ip_addresses = []
    for line in raw_ip_list:
        re_search = ip_src_re.search(line)
        if re_search:
            ip_addresses.append(re_search.group(1))
    return ip_addresses

def create_email(sender_email, recipient_email, pi_name, ip_addresses):
    """Creates email message that contains local IP address.

    sender_email        string of sender's Gmail address
    recipient_email     string of recipient's email address
    ip_addresses        list of strings of ip addresses

    returns             string of flattened MIMEText of email message
                        containing ip address
    """
    ip_addresses = (' | ').join(ip_addresses)
    message = MIMEText('')
    message['Subject'] = '[{}] {}'.format(pi_name, ip_addresses)
    message['From'] = sender_email
    message['To'] = recipient_email
    return message.as_string()

def send_email(sender_email, sender_password, recipient_email, email_message):
    """Sends email_message to recipient_email using sender_email and
    sender_password.

    sender_email        string of sender's Gmail address
    sender_password     string of sender's Gmail password
    recipient_email     string of recipient's email address
    email_message       string of flattened MIMEText of email message
    """
    mail_server = SMTP(host='smtp.gmail.com', port=587)
    mail_server.ehlo()      # extended hello
    mail_server.starttls()  # encrypt transfer with TLS
    mail_server.ehlo()
    mail_server.login(sender_email, sender_password)
    mail_server.sendmail(sender_email, [recipient_email], email_message)
    mail_server.quit()

def main(argv):
    """Main function"""

    help_text = """CODE! v1.0

Usage:
  python CODE.py [options]

Options:

  -h, --help                help
  -t, --test                test"""

    try:
        opts, args = getopt.getopt(argv, "hts", ["help", "test", "stress"])
    except getopt.GetoptError:
        print(args)
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg)
            print(help)
            sys.exit()
        elif opt in ("-t", "--test"):
            test()
            sys.exit()
        elif opt in ("-s", "--stress"):
            stress()
            sys.exit()
    ip_addresses = get_ip_addresses()
    email_message = create_email(
        SENDER_GMAIL,
        RECIPIENT_EMAIL,
        PI_NAME,
        ip_addresses
        )
    send_email(
        SENDER_GMAIL,
        SENDER_PASSWORD,
        RECIPIENT_EMAIL,
        email_message
        )

def test():
    """Runs doctest on functions."""

    import doctest
    print(doctest.testmod())

def stress():
    """Runs stress test on functions."""

    print("STRESS TEST")
    import timeit
    print(timeit.timeit(
        # edit stress test function here
        'FUNCTION()',
        number=1,
        setup="from __main__ import FUNCTION",
        )
         )

if __name__ == '__main__':
    main(sys.argv[1:])
