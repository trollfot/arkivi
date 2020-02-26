import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SecureMailer(object):

    def __init__(self, host, username, password, port="25", debug=False):
        self.mailer = None
        self.host = host
        self.port = port
        self.debug = debug
        self.username = username
        self.password = password

    def __enter__(self):
        server = smtplib.SMTP(self.host, self.port)
        server.set_debuglevel(self.debug)

        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        server.login(self.username, self.password)
        self.mailer = server
        return server.sendmail

    def __exit__(self, type, value, traceback):
        self.mailer.close()


def make_email(emitter, recipient, subject, text, html=None):
    msg = MIMEMultipart('alternative')
    msg['From'] = emitter
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_charset('utf-8')

    part1 = MIMEText(text, 'plain')
    part1.set_charset('utf-8')
    msg.attach(part1)

    if html is not None:
        part2 = MIMEText(html, 'html')
        part2.set_charset('utf-8')
        msg.attach(part2)

    return msg
