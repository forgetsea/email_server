import schedule
import time
from pathlib import Path

from src.excel_utils import read_all_emails
from src.sent_tracker import load_sent_emails, save_sent_emails
from src.email_utils import send_email_batch
from src.config import EMAIL_SUBJECT, BATCH_LIMIT, RECIPIENT_LIMIT, EMAIL_TEMPLATE_PATH,EXCEL_FOLDER,SENT_RECORD_FILE

# loading emails
all_emails = read_all_emails(EXCEL_FOLDER)
sent_emails = load_sent_emails(SENT_RECORD_FILE)
remaining_emails = list(all_emails - sent_emails)
print(f"all emails: {len(all_emails)}, pending send: {len(remaining_emails)}")


# send email
def send_batches():
    global remaining_emails, sent_emails
    for _ in range(BATCH_LIMIT):
        if not remaining_emails:
            print("All emails have been sent")
            return
        batch = remaining_emails[:RECIPIENT_LIMIT]
        send_email_batch(batch, EMAIL_SUBJECT, EMAIL_TEMPLATE_PATH)
        sent_emails.update(batch)
        remaining_emails = remaining_emails[RECIPIENT_LIMIT:]
        save_sent_emails(SENT_RECORD_FILE, sent_emails)
        time.sleep(10)  

# 21:00 process
# schedule.every().day.at("21:00").do(send_batches)

print("waiting to process")
send_batches()

# # permentally running
# while True:
#     schedule.run_pending()
#     time.sleep(60)
