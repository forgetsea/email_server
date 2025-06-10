import re
from pathlib import Path

def extract_emails_from_file(filepath):
    text = Path(filepath).read_text(encoding='utf-8')

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    emails = re.findall(email_pattern, text)
    
    return sorted(set(emails))

# 示例调用
emails = extract_emails_from_file('../temp/temp.txt')

Path("output_emails.txt").write_text('\n'.join(emails))