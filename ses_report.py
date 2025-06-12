import boto3
import json
import os
from src.config import *
from datetime import datetime

QUEUE_URL = AWS_SQS_URL
BOUNCED_FILE = 'temp/ses_report/bounced_emails.json'
UNSUBSCRIBED_FILE = 'temp/ses_report/unsubscribe.json'
COMPLAINED_FILE = 'temp/ses_report/complaint.json'

MAX_PULL = 10000
WAIT_TIME = 5


# 初始化 SQS 客户端
sqs = boto3.client(
    'sqs',
    region_name='us-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def load_email_set(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(json.load(f))


def save_email_set(email_set, file_path):
    with open(file_path, 'w') as f:
        json.dump(sorted(email_set), f, indent=2)


def process_feedback_event(feedback, unsubscribed_emails, bounced_emails, complained_emails):
    type_ = feedback.get("eventType") or feedback.get("notificationType")
    destination = feedback.get("mail", {}).get("destination", [])

    if type_ == "Unsubscribe":
        for email in destination:
            unsubscribed_emails.add(email)
            print(f"[UNSUBSCRIBE] {email}")
    elif type_ == "Bounce":
        recipients = feedback.get("bounce", {}).get("bouncedRecipients", [])
        for r in recipients:
            email = r.get("emailAddress")
            if email:
                bounced_emails.add(email)
                print(f"[BOUNCE] {email}")
    elif type_ == "Complaint":
        recipients = feedback.get("complaint", {}).get("complainedRecipients", [])
        for r in recipients:
            email = r.get("emailAddress")
            if email:
                complained_emails.add(email)
                print(f"[COMPLAINT] {email}")


def pull_sqs_feedback():
    unsubscribed_emails = load_email_set(UNSUBSCRIBED_FILE)
    bounced_emails = load_email_set(BOUNCED_FILE)
    complained_emails = load_email_set(COMPLAINED_FILE)

    pulled = 0

    while pulled < MAX_PULL:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=WAIT_TIME
        )

        messages = response.get("Messages", [])
        if not messages:
            break

        for msg in messages:
            try:
                body_raw = msg['Body']
                body = json.loads(body_raw)

                message_raw = body.get("Message", "")
                if not message_raw.strip().startswith("{"):
                    print("[INFO] Skipped non-event message:", message_raw)
                    continue
                feedback = json.loads(message_raw)
                process_feedback_event(feedback, unsubscribed_emails, bounced_emails, complained_emails)

                # 删除消息
                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=msg['ReceiptHandle']
                )
                pulled += 1
                if pulled >= MAX_PULL:
                    break
            except Exception as e:
                print(f"[ERROR] Failed to process message: {e}")

    # 保存结果
    save_email_set(unsubscribed_emails, UNSUBSCRIBED_FILE)
    save_email_set(bounced_emails, BOUNCED_FILE)
    save_email_set(complained_emails, COMPLAINED_FILE)

    print(f"\n all processed, total: {pulled}")
    print(f"unsubscribed: {len(unsubscribed_emails)}")
    print(f"bounced: {len(bounced_emails)}")
    print(f"complaints: {len(complained_emails)}")


# 执行主函数
if __name__ == '__main__':
    print(f"start pull: {datetime.now()}")
    pull_sqs_feedback()

