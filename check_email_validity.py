import re
import smtplib
import DNS


class MXRecord:
    _domain = None
    _priority = None
    _exchange = None

    def __init__(self, priority=None, exchange=None, domain=None):
        self._priority = priority
        self._exchange = exchange
        self._domain = domain

    @property
    def priority(self):
        return self._priority

    @property
    def exchange(self):
        return self._exchange

    @property
    def domain(self):
        return self._domain


def get_mx_records(domain):
    """
    Gets an array of MXRecords associated to the domain specified.

    :param domain:
    :return: [MXRecord]
    """
    DNS.DiscoverNameServers()
    request = DNS.Request()
    response = request.req(name=domain, qtype=DNS.Type.MX)

    mx_records = []
    for answer in response.answers:
        mx_records.append(MXRecord(priority=answer['data'][0], exchange=answer['data'][1], domain=domain))

    return sorted(mx_records, key=lambda record: record.priority)


def check_email_validity(recipient_address, sender_address, smtp_timeout=10, helo_hostname=None):
    """


    :param recipient_address:
    :param sender_address:
    :param smtp_timeout:
    :param helo_hostname:
    :return: dict
    """
    domain = str.lower(recipient_address[recipient_address.find('@') + 1:])
    if helo_hostname is None:
        helo_hostname = domain

    records = get_mx_records(helo_hostname)
    ret = {'status': None, 'extended_status': None, 'message': None}

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
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            ret['status'] = 111
            ret['message'] = "Connection refused or unable to open an SMTP stream."

    return ret
