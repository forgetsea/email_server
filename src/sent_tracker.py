import pickle
import os

def load_sent_emails(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return set()

def save_sent_emails(file_path, sent_emails):
    with open(file_path, 'wb') as f:
        pickle.dump(sent_emails, f)