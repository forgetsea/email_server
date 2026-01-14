import os
import pandas as pd
from pathlib import Path
import unicodedata
import re
import logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler() 
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('log/sum_excel.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def clean_email(email):
    email = unicodedata.normalize('NFKC', email)  # 将全角符号变半角
    email = re.sub(r'\s+', '', email)             # 去除所有空白字符
    email = email.replace('\u200b', '')           # 去除零宽字符
    return email.strip().lower()

def read_excel(folder_path):
	all_emails = set()
	for file in Path(folder_path).glob('*.xlsx'):
		df = pd.read_excel(file, engine='openpyxl')
		emails = df.iloc[:,0].dropna().astype(str).apply(clean_email)
		all_emails.update(emails)
		logger.info(f"Processed file:{file.name}, include {len(emails)} emails")
	logger.info(f"Total {len(all_emails)} emails")
	return all_emails

def output_excel(emails, output_path):
	# emails is set()
	try:
		if emails:
			df = pd.DataFrame(list(emails),columns=['Email'])
			df.to_excel(output_path, index=False, engine='openpyxl')
	except Exception as e:
		raise e

# combine files under folder and dedup
logger.info("Start sum emails")
path = 'temp/'
output_path = 'temp/sum/emails.xlsx'
emails = read_excel(path)
output_excel(emails, output_path)
logger.info("Finished-----")