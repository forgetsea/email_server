import pickle
import os
import json

def load_sent_emails(file_path):
    if not os.path.exists(file_path):
        return set()
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Failed to load sent_emails: {e}")
        return set()

def save_sent_emails(file_path, sent_emails):
    with open(file_path, 'wb') as f:
        pickle.dump(sent_emails, f)


def load_ses_emails(path):
    emails = set()
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            filepath = os.path.join(path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    email_list = json.load(file)
                    if isinstance(email_list, list):
                        emails.update(email_list)
                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")
    return emails