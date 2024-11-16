import requests
import argparse
import sys
import time
from datetime import datetime



def check_mails(parameter):
    # The Have I Been Pawned API Key and URL
    hibp_api_key = "ab62cea28a114653909fa9ef1547d590"
    base_url = "https://haveibeenpwned.com/api/v3"

    # Building the header used to call the API
    headers = {
        "hibp-api-key": hibp_api_key,
        "user-agent": "PythonApp"  # Custom user-agent
    }

    
    # Check the DataBase for each email provided as a command line argument
    
    response = requests.get(f"{base_url}/breachedaccount/{parameter}", headers=headers)
    # Handle the response
    if response.status_code == 200:
        print("Breaches found:")
        print(response.json())
        return 1  # Parse the JSON response
    elif response.status_code == 404:
        print("No breaches found for this account.")
        return 0
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return -1

