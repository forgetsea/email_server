from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../

#Update email info
EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/IAG933.html'
EMAIL_SUBJECT = 'IAG933 – Inhibitor of YAP/TAZ–TEAD Interaction'

SENT_RECORD_FILE = BASE_DIR /'temp/sent/sent_emails_IAG933.pkl'
LOG_FILE = BASE_DIR / 'logs/IAG933.log'