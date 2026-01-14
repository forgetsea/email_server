from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src/../

#Update email info
EMAIL_TEMPLATE_PATH = BASE_DIR / 'templates/PLX.html'
EMAIL_SUBJECT = '$450/g, Special Offer on PLX-5622 for Microglia Research'

SENT_RECORD_FILE = BASE_DIR /'temp/sent/PLX.pkl'
LOG_FILE = BASE_DIR / 'logs/PLX.log'