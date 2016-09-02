import re
import smtplib


def check_email_status(mx_resolver, recipient_address, sender_address, smtp_timeout=10, helo_hostname=None):
    """
    Checks if an email might be valid by getting the status from the SMTP server.

    :param mx_resolver: MXResolver
    :param recipient_address: string
    :param sender_address: string
    :param smtp_timeout: integer
    :param helo_hostname: string
    :return: dict
    """
    domain = str.lower(recipient_address[recipient_address.find('@') + 1:])
    if helo_hostname is None:
        helo_hostname = domain

    records = mx_resolver.get_mx_records(helo_hostname)
    ret = {'status': 101, 'extended_status': None, 'message': "The server is unable to connect."}

    smtp = smtplib.SMTP(timeout=smtp_timeout)

    for mx in records:
        try:
            connection_status, connection_message = smtp.connect(mx.exchange)
            if connection_status == 220:
                smtp.helo(domain)
                smtp.mail(sender_address)
                status, message = smtp.rcpt(recipient_address)
                ret['status'] = status

                pattern = re.compile('(\d+\.\d+\.\d+)')
                matches = re.match(pattern, message)
                if matches:
                    ret['extended_status'] = matches.group(1)

                ret['message'] = message
            smtp.quit()
            break
        except smtplib.SMTPConnectError:
            ret['status'] = 111
            ret['message'] = "Connection refused or unable to open an SMTP stream."
        except smtplib.SMTPServerDisconnected:
            ret['status'] = 111
            ret['extended_status'] = "SMTP Server disconnected"

    return ret


if __name__ == "__main__":
    try:
        console_input = raw_input
    except NameError:
        console_input = input

    recipient_email = console_input("Recipient Email: ")
    sender_email = console_input("Sender Email: ")
    from resolvers import PyDNSMXResolver

    print(check_email_status(PyDNSMXResolver, recipient_email, sender_email))
