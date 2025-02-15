import random
import string
from datetime import datetime, timedelta, timezone

def generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

def generate_otp_expiry() -> datetime:
    """Generate OTP expiry time (15 minutes from now)"""
    return datetime.now(timezone.utc) + timedelta(minutes=15)
