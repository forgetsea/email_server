from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../

#Update email info
EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/EGFR.html'
EMAIL_SUBJECT = 'High-Purity EGFR Inhibitors — Osimertinib & EGFR-IN-11'

SENT_RECORD_FILE = BASE_DIR /'temp/sent/EGFR.pkl'
LOG_FILE = BASE_DIR / 'logs/EGFR.log'