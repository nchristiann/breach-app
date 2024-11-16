import hashlib
import requests
import time
import subprocess
from generate_rand_password import generate_password

# Function to check if a password has been pwned
def check_password(password):
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
                return 1
        print(f"Password '{password}' has not been pwned.")
        return 0
    elif response.status_code == 404:
        print(f"Password '{password}' has not been pwned.")
        return 0
    else:
        print(f"Error checking password '{password}': {response.status_code}")
        return -1

# Function to check multiple passwords sequentially
def check_multiple_passwords(passwords):
    for password in passwords:
        print(f"Checking password: {password}")
        if(check_password(password)):
            print("Your password has been breached you should change it")
            print("Do you want a random password? Y/N")
            answer = input()
            if answer == "Y":
                print(generate_password())
            else:
                print("Goodbye")
        time.sleep(1)  # Delay between requests to respect rate limit

# Example list of passwords to check
passwords_to_check = [
    "password123",
    "qwerty123",
    "letmein",
    "BAM@bam13!",
    "georgelupnemuritotu"
]

# Check the example passwords\
check_multiple_passwords(passwords_to_check)


