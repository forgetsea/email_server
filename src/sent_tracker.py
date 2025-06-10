import pickle
import os

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