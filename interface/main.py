import hashlib
import requests
import time
import subprocess

# Function to check if a password has been pwned
def check_pass(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]  # First 5 characters of the hash
    suffix = sha1_hash[5:]  # Remaining part of the hash

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code == 200:
        # Check if the suffix matches any hashes in the response
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                print(f"Password '{password}' has been pwned {count} times!")
                return "Password has been breached"
        print(f"Password '{password}' has not been pwned.")
        return "Password is safe"
    elif response.status_code == 404:
        print(f"Password '{password}' has not been pwned.")
        return "Password is safe"
    else:
        print(f"Error checking password '{password}': {response.status_code}")
        return -1



