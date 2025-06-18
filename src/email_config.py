from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../

#Update email info
EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/GBM_PLX5622_CN.html'
EMAIL_SUBJECT = 'PLX-5622 – A Tool for Studying Microglia in GBM Recurrence, 设有中国总代理'

SENT_RECORD_FILE = BASE_DIR /'temp/sent/sent_emails_GBM5622.pkl'
LOG_FILE = BASE_DIR / 'logs/GBM5622.log'