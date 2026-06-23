import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode('utf-8')).hexdigest()

def validate_input(text):
    forbidden = ["'", '"', ";", "--"]
    for char in forbidden:
        text = text.replace(char, "")
    return text.strip()