import pandas as pd
from pathlib import Path

def read_all_emails(folder_path):
    all_emails = set()
    for file in Path(folder_path).glob('*.xlsx'):
        df = pd.read_excel(file, engine='openpyxl')
        emails = df.iloc[:, 0].dropna().astype(str).str.strip()
        all_emails.update(emails)
    return all_emails