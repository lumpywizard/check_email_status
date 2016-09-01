from check_email_validity import check_email_validity

try:
    console_input = raw_input
except NameError:
    console_input = input

if __name__ == "__main__":
    recipient_email = console_input("Recipient Email: ")
    sender_email = console_input("Sender Email: ")
    print(check_email_validity(recipient_email, sender_email))
