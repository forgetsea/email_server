import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from .config import *
from .logger_utils import logger
from .sent_tracker import load_sent_emails, save_sent_emails

MAX_RETRIES = 3

def build_email_content(batch_emails, subject, template_path, address):
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = address
    msg['To'] = address
    msg['Bcc'] = ','.join(batch_emails)
    msg['List-Unsubscribe'] = '<mailto:tech@chemgood.com?subject=unsubscribe>'
    msg['X-SES-CONFIGURATION-SET'] = 'my-first-configuration-set'

    # load template
    html_body = Path(template_path).read_text(encoding='utf-8')
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, 'html'))

    return msg

def send_email_batch_gmail(batch_emails, subject, template_path, account):
    # for google use
    try:
        msg = build_email_content(batch_emails, subject, template_path, EMAIL_ADDRESS)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(account["user"], account["pass"])
            smtp.send_message(msg)
        logger.info(f"Already send {len(batch_emails)} emails")
    except Exception as e:
        logger.error(f"Failed: {str(e)} | emails: {batch_emails}")


def send_one_email_SES(email, subject, template_path, account):
    for attempt in range(MAX_RETRIES):
        try:
            smtp_send_SES(email, subject, template_path, account)
            return True  # 成功
        except smtplib.SMTPAuthenticationError as e:
            logger.critical(f"[FATAL] SMTP Authentication failed: {e}")
            raise SystemExit("Stopped: Invalid SMTP credentials.")
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            logger.warning(f"[Retry {attempt+1}] SMTP server unavailable: {e}")
            time.sleep(5)
        except smtplib.SMTPSenderRefused as e:
            logger.error(f"[Sender Refused] Check sender email: {e}")
            return False
        except smtplib.SMTPRecipientsRefused as e:
            logger.warning(f"[Recipients Refused] Invalid emails in batch: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.warning(f"[SMTP Error] General SMTP error: {e}")
            return False
        except Exception as e:
            logger.exception(f"[Unexpected Error] {e}")
            return False
    logger.error("[MAX RETRIES EXCEEDED] Giving up on this batch.")
    return False

def smtp_send_SES(remaining_emails, subject, template_path, account, sent_emails, SENT_RECORD_FILE):
    #Amazon SES 
    html_template = load_template_body(template_path)
    MAX_PER_SESSION=300
    index = 0
    total_emails = len(remaining_emails)
    while index < total_emails:
        try:
            with smtplib.SMTP_SSL(SES_SMTP_SERVER, SES_SMTP_PORT) as smtp:
                smtp.login(account["user"], account["pass"])
                logger.info(f"SMTP connection established. Sending index{index}")

                session_count = 0
                while session_count < MAX_PER_SESSION and index < total_emails:
                    recipient = remaining_emails[index]
                    if index >= SES_MAX_DAILY_LIMIT:
                        logger.warning("Daily SES limit reached.")
                        break

                    msg = build_personal_email(recipient, subject, html_template, EMAIL_ADDRESS)
                    try:
                        smtp.send_message(msg)
                        sent_emails.add(recipient)
                        save_sent_emails(SENT_RECORD_FILE, sent_emails)
                        session_count += 1
                        logger.debug(f"[{index}] Sent to: {recipient}")
                    except Exception as e:
                        logger.error(f"Failed to send to {recipient}: {e}")
                    index += 1
                    #1seconds 10email    
                    time.sleep(0.1) 
        except smtplib.SMTPAuthenticationError as e:
            logger.critical(f"SMTP authentication failed: {e}")
            raise SystemExit("Stopped due to invalid SMTP credentials.")
        except Exception as e:
            logger.critical(f"Unexpected failure: {e}")
            raise

def load_template_body(template_path):
    return Path(template_path).read_text(encoding='utf-8')

def build_personal_email(recipient, subject, html_body, sender):
    # Create a multipart message with HTML content
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    msg['Reply-To'] = 'info@chemgood.com'
    # Unsubscribe header (RFC compliant)
    msg['List-Unsubscribe'] = '<mailto:tech@chemgood.com?subject=unsubscribe>'
    msg['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
    msg['X-SES-CONFIGURATION-SET'] = 'my-first-configuration-set'

    # Optionally add plain text fallback
    plain_text = subject

    msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))


    return msg