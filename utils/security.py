import re
from flask import abort

def validate_input(input_value):
    if not input_value or not isinstance(input_value, str) or len(input_value) > 255:
        abort(400, "Invalid input")
    # Further validations can be added here (e.g., regex for phone number)
    return input_value

def encrypt_data(data):
    # Use cryptography library to encrypt data
    pass

def decrypt_data(encrypted_data):
    # Use cryptography library to decrypt data
    pass