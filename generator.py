import os
import base64
import hashlib

def generate_key():
    # Generate a secure key for encryption
    return base64.urlsafe_b64encode(os.urandom(32))

def generate_password(length=64, user_data=''):
    # Combine random bytes with user-specific data
    random_bytes = os.urandom(length)
    combined_data = random_bytes + user_data.encode()
    
    # Hash the combined data using SHA-3 (quantum-resistant)
    password = hashlib.sha3_256(combined_data).digest()
    
    # Encode the password in a URL-safe base64 format
    return base64.urlsafe_b64encode(password).decode()
