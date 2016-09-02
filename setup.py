from setuptools import setup

setup(
    name="check_email_status",
    description="Check the existence of a mailbox via SMTP.",
    version="1.0",
    install_requires=[
        "pyDNS",
        "dnspython"
    ],
    author="Adrien Howard",
    author_email="lumpywizard@gmail.com",
    url="https://github.com/lumpywizard/check_email_status"
)
