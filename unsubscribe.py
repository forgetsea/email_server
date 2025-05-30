import imaplib
import email
from email.header import decode_header
import pandas as pd
from pathlib import Path

from src.config import EMAIL_ADDRESS,EMAIL_PASSWORD

UNSUBSCRIBE_FILE = Path('./unsubscribe_list.csv')

def fetch_unsubscribed():
    # connect gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # choose inbox
    imap.select("INBOX")

    # search
    status, messages = imap.search(None, '(SUBJECT "unsubscribe")')
    email_ids = messages[0].split()

    unsub_emails = set()

    for e_id in email_ids:
        status, msg_data = imap.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                unsub_emails.add(email.utils.parseaddr(msg.get("From"))[1])

    # save
    if UNSUBSCRIBE_FILE.exists():
        df = pd.read_csv(UNSUBSCRIBE_FILE)
        unsub_emails.update(df['email'].dropna())

    df = pd.DataFrame({"email": list(unsub_emails)})
    df.to_csv(UNSUBSCRIBE_FILE, index=False)
    print(f"updated {len(unsub_emails)} unsubscribe mail")

    imap.logout()

fetch_unsubscribed()
