import uuid

def generate_verification_code_alphanumeric():
    """
    Generates a unique alphanumeric verification code.

    Returns:
        str: A 5-character alphanumeric code.
    """
    return uuid.uuid4().hex[:5].upper()
