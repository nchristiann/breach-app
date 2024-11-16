import requests
import argparse
import sys

hibp_api_key = "ab62cea28a114653909fa9ef1547d590"

base_url = "https://haveibeenpwned.com/api/v3"

email = "nekulachristy@gmail.com"

headers = {
    "hibp-api-key": hibp_api_key,
    "user-agent": "PythonApp"  # Custom user-agent
}

# Make the request

counter = len(sys.argv) - 1



for i in range(counter) :
    response = requests.get(f"{base_url}/breachedaccount/{sys.argv[i+1]}", headers=headers)

    # Handle the response
    if response.status_code == 200:
        print("Breaches found:")
        print(response.json())  # Parse the JSON response
    elif response.status_code == 404:
        print("No breaches found for this account.")
    else:
        print(f"Error: {response.status_code} - {response.text}")



