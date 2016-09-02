check_email_status
=======================

This package exists to help poll smtp servers to see if a mailbox address is valid.
It doesn't return true or false, but a set of status codes, extended status codes,
and full messages from the responding server.

Usage
======================

Here is an example using pyDNS as the MX resolver::

    from check_email_status import check_email_status
    from check_email_status.resolvers import PyDNSMXResolver

    status = check_email_status(PyDNSMXResolver, 'recipient@domain.com', 'sender@domain.com')

    # This is the SMTP status code returned by the server. (e.g.) 550
    print status['status']

    # This is the extended status code, for instance 5.1.1 would mean the account doesn't exist.
    # If an extended code is not sent, this is not set.
    print status['extended_status']

    # This is the message returned from the mail server describing the results of the query.
    print status['messsage']

