import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from .config import EMAIL_ADDRESS, EMAIL_PASSWORD
from .logger_utils import logger

def build_email_content(batch_emails, subject, template_path):
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Bcc'] = ','.join(batch_emails)
    msg['List-Unsubscribe'] = '<mailto:tech@chemgood.com?subject=unsubscribe>'

    # load template
    html_body = Path(template_path).read_text(encoding='utf-8')
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, 'html'))

    return msg

def send_email_batch(batch_emails, subject, template_path):
    try:
        msg = build_email_content(batch_emails, subject, template_path)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Already sent {msg['Bcc'].count(',') + 1} emails")
        logger.info(f"Already send {len(batch_emails)} emails: {batch_emails}")
    except Exception as e:
        logger.error(f"Failed: {str(e)} | emails: {batch_emails}")