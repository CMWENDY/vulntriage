import hashlib


def hash_password(password):
    """Store the user's password."""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash


def legacy_token(user_id):
    return hashlib.sha1(str(user_id).encode()).hexdigest()
