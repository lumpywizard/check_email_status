from setuptools import setup

setup(
    name="check_email_status",
    packages=['check_email_status'],
    description="Check the existence of a mailbox via SMTP.",
    version="1.1.2",
    install_requires=[
        "pyDNS"
    ],
    author="Adrien Howard",
    author_email="lumpywizard@gmail.com",
    url="https://github.com/lumpywizard/check_email_status",
    download_url="https://github.com/lumpywizard/check_email_status/tarball/1.1.2",
    keywords=['smtp', 'validation', 'status', 'mailbox', 'email'],
    classifiers=[],
)
