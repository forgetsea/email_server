import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../
load_dotenv(dotenv_path=BASE_DIR / '.env')

#google email server
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

RECIPIENT_LIMIT = int(os.getenv('RECIPIENT_LIMIT', 100))
BATCH_LIMIT = int(os.getenv('BATCH_LIMIT', 5))

#email load directory
EXCEL_FOLDER = BASE_DIR / 'files'

#Amazon email server
SES_ACCOUNT = os.getenv('SES_SMTP_USERNAME')
SES_PASSWORD = os.getenv('SES_SMTP_PASSWORD')

SES_RATE_LIMIT = int(os.getenv('SES_RATE_LIMIT'))
SES_MAX_DAILY_LIMIT = int(os.getenv('SES_MAX_DAILY_LIMIT'))
SES_SMTP_SERVER = os.getenv('SES_SMTP_SERVER')
SES_SMTP_PORT = int(os.getenv('SES_SMTP_PORT'))

#Amazon Simple queue services setting, to receive feedback
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SQS_URL=os.getenv('AWS_SQS_URL')

#Update email info
EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/BI2865_CN.html'
SENT_RECORD_FILE = BASE_DIR /'temp/sent/sent_emails_BI2865.pkl'
EMAIL_SUBJECT = 'BI-2865, Potent Pan-KRAS Inhibitor--设有中国总代理'
LOG_FILE = BASE_DIR / 'logs/BI2865.log'