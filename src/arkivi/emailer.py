import smtplib
import functools
from contextlib import contextmanager
from collections import namedtuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_CONFIG = namedtuple(
    'SMTP', ['host', 'user', 'password', 'port', 'emitter', 'recipient'])


class SecureMailer:

    def __init__(self, debug=False, **config):
        self.config = SMTP_CONFIG(**config)
        self.debug = debug

    @staticmethod
    def format_email(_from, _to, subject, text, html=None):
        msg = MIMEMultipart('alternative')
        msg['From'] = _from
        msg['To'] = _to
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

    def email(self, subject, text, html=None):
        return self.format_email(
            self.config.emitter, self.config.recipient,
            subject, text, html)

    @contextmanager
    def smtp(self):
        server = smtplib.SMTP(self.config.host, self.config.port)
        server.set_debuglevel(self.debug)

        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        server.login(self.config.user, self.config.password)
        try:
            yield functools.partial(
                server.sendmail, self.config.emitter, self.config.recipient)
        finally:
            server.close()
