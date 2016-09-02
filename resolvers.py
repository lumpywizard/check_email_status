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


class MXResolver:
    """
    Gets an array of MXRecords associated to the domain specified.

    :param domain:
    :return: [MXRecord]
    """
    @staticmethod
    def get_mx_records(domain):
        return []


class PyDNSMXResolver(MXResolver):
    @staticmethod
    def get_mx_records(domain):
        """
        Gets an array of MXRecords associated to the domain specified.

        :param domain:
        :return: [MXRecord]
        """
        import DNS

        DNS.DiscoverNameServers()
        request = DNS.Request()
        response = request.req(name=domain, qtype=DNS.Type.MX)

        mx_records = []
        for answer in response.answers:
            mx_records.append(MXRecord(priority=answer['data'][0], exchange=answer['data'][1], domain=domain))

        return sorted(mx_records, key=lambda record: record.priority)


class DNSPythonMXResolver(MXResolver):
    @staticmethod
    def get_mx_records(domain):
        """
        Gets an array of MXRecords associated to the domain specified.

        :param domain:
        :return: [MXRecord]
        """
        import dns.resolver

        response = dns.resolver.query(domain, 'MX')

        mx_records = []
        for answer in response.answers:
            mx_records.append(MXRecord(priority=answer.preference, exchange=answer.exchange, domain=domain))

        return sorted(mx_records, key=lambda record: record.priority)
