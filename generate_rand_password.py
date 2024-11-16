import string
import secrets
import re

def generate_password(length=16, min_digits=2, min_special=2, min_upper=2, min_lower=2):
    """
    Generate a cryptographically secure random password. 
    Args:
        length (int): Desired password length (default: 16)
        min_digits (int): Minimum number of digits (default: 2)
        min_special (int): Minimum number of special characters (default: 2)
        min_upper (int): Minimum number of uppercase letters (default: 2)
        min_lower (int): Minimum number of lowercase letters (default: 2)
        
    Returns:
        str: A random password meeting the specified criteria
    """
    # Validate minimum requirements
    if length < (min_digits + min_special + min_upper + min_lower):
        raise ValueError("Length too short to satisfy minimum requirements")
    # Character sets
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    # Generate required characters
    password = []
    password.extend(secrets.choice(digits) for _ in range(min_digits))
    password.extend(secrets.choice(special) for _ in range(min_special))
    password.extend(secrets.choice(uppercase) for _ in range(min_upper))
    password.extend(secrets.choice(lowercase) for _ in range(min_lower))
        # Fill remaining length with random characters from all sets
    all_chars = digits + special + uppercase + lowercase
    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password
    shuffled = list(password)
    secrets.SystemRandom().shuffle(shuffled)
    final_password = ''.join(shuffled)
    
    # Verify requirements are met
    if not all([
        len(re.findall(r'\d', final_password)) >= min_digits,
        len(re.findall(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', final_password)) >= min_special,
        len(re.findall(r'[A-Z]', final_password)) >= min_upper,
        len(re.findall(r'[a-z]', final_password)) >= min_lower
    ]):
        # Recursively try again if requirements not met (rare due to explicit character inclusion)
        return generate_password(length, min_digits, min_special, min_upper, min_lower)
        
    return final_password