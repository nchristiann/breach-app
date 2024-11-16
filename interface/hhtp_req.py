import requests
import argparse
import sys

hibp_api_key = "ab62cea28a114653909fa9ef1547d590"
base_url = "https://haveibeenpwned.com/api/v3"

headers = {
    "hibp-api-key": hibp_api_key,
    "user-agent": "PythonApp"  # Custom user-agent
}

def check_breach(email):
    response = requests.get(f"{base_url}/breachedaccount/{email}", headers=headers)
    if response.status_code == 200:
        return f"{email}: Breached! Details: {response.json()}"
    elif response.status_code == 404:
        return f"{email}: No breach found."
    else:
        return f"{email}: Error {response.status_code} - {response.text}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if an email has been breached.")
    parser.add_argument("emails", metavar="E", type=str, nargs="+", help="Email(s) to check")
    args = parser.parse_args()

    for email in args.emails:
        print(check_breach(email))



