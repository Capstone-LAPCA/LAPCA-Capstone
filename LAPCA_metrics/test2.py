import mailbox
import email
import re
def get_email_body(msg):
    if msg.is_multipart():
        return get_email_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)