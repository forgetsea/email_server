import time
from pathlib import Path

from src.excel_utils import read_all_emails
from src.sent_tracker import load_sent_emails, save_sent_emails, load_ses_emails
from src.email_utils import send_email_batch_gmail,smtp_send_SES
from src.logger_utils import logger
from src.config import *


import os
import json

# 确保脚本运行目录正确
os.chdir(BASE_DIR)

# loading emails
all_emails = read_all_emails(EXCEL_FOLDER)
sent_emails = load_sent_emails(SENT_RECORD_FILE)

complain_emails = load_ses_emails(JSON_FOLDER)
remaining_emails = list(all_emails - sent_emails - complain_emails)
logger.info(f"all emails: {len(all_emails)}, pending send: {len(remaining_emails)}")
logger.info(f"Will send Title: {EMAIL_SUBJECT}. Using template {EMAIL_TEMPLATE_PATH}")

account = {"user": SES_ACCOUNT, "pass": SES_PASSWORD}

# send email
def send_batches():
    global remaining_emails, sent_emails
    for _ in range(BATCH_LIMIT):
        if not remaining_emails:
            logger.info("All emails have been sent")
            return
        batch = remaining_emails[:RECIPIENT_LIMIT]
        send_email_batch_gmail(batch, EMAIL_SUBJECT, EMAIL_TEMPLATE_PATH, account)
        sent_emails.update(batch)
        remaining_emails = remaining_emails[RECIPIENT_LIMIT:]
        save_sent_emails(SENT_RECORD_FILE, sent_emails)
        logger.info(f"pending send: {len(remaining_emails)}")

# system auto
logger.debug("waiting to process")
# send_batches()
smtp_send_SES(
    remaining_emails=remaining_emails,
    subject=EMAIL_SUBJECT,
    template_path=EMAIL_TEMPLATE_PATH,
    account=account,
    sent_emails=sent_emails,
    SENT_RECORD_FILE=SENT_RECORD_FILE
)
logger.debug("All finished")