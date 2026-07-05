import secrets

def generate_code(length=6):
    return secrets.token_urlsafe(length)[:length]