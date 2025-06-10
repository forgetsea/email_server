import boto3
import json
import os
from src.config import *

QUEUE_URL = AWS_SQS_URL
BOUNCED_EMAILS_FILE = 'logs/bounced_emails.json'
MAX_MESSAGES = 10
WAIT_TIME = 5


# 初始化 SQS 客户端
sqs = boto3.client(
    'sqs',
    region_name='us-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 加载本地已有的退信邮箱
def load_bounced_emails():
    if not os.path.exists(BOUNCED_EMAILS_FILE):
        return set()
    with open(BOUNCED_EMAILS_FILE, 'r') as f:
        return set(json.load(f))

# 保存邮箱到文件
def save_bounced_emails(emails):
    with open(BOUNCED_EMAILS_FILE, 'w') as f:
        json.dump(sorted(list(emails)), f, indent=2)

# 拉取消息并提取失败邮箱
def pull_feedback():
    bounced_emails = load_bounced_emails()
    print("Loaded existing:", len(bounced_emails))

    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=MAX_MESSAGES,
        WaitTimeSeconds=WAIT_TIME
    )

    messages = response.get('Messages', [])
    print("Pulled:", len(messages))

    for msg in messages:
        try:
            body = json.loads(msg['Body'])
            feedback = json.loads(body['Message'])
            type_ = feedback.get("notificationType")

            if type_ == "Bounce":
                recipients = feedback.get("bounce", {}).get("bouncedRecipients", [])
                for r in recipients:
                    email = r.get("emailAddress")
                    if email:
                        bounced_emails.add(email)
                        print(f" Bounced: {email}")

            elif type_ == "Complaint":
                recipients = feedback.get("complaint", {}).get("complainedRecipients", [])
                for r in recipients:
                    email = r.get("emailAddress")
                    if email:
                        bounced_emails.add(email)
                        print(f"Complaint: {email}")

            # 删除处理完的消息
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg['ReceiptHandle']
            )

        except Exception as e:
            print("Error:", e)

    # 保存更新后的退信邮箱
    save_bounced_emails(bounced_emails)
    print(f"Total saved bounced emails: {len(bounced_emails)}")

# 主程序执行
if __name__ == "__main__":
    pull_feedback()
