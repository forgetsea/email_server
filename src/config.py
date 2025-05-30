import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../
load_dotenv(dotenv_path=BASE_DIR / '.env')

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

RECIPIENT_LIMIT = int(os.getenv('RECIPIENT_LIMIT', 100))
BATCH_LIMIT = int(os.getenv('BATCH_LIMIT', 10))

EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/email_template.html'
# EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/email_template_CN.html'
EXCEL_FOLDER = BASE_DIR / 'files'

SENT_RECORD_FILE = 'sent_emails.pkl'
EMAIL_SUBJECT = 'Daily notice'