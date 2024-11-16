import json 
import time
from hhtp_req import check_mails

with open('interface/emails.json') as file:
    data = json.load(file)
    emails = data['emails']

while(1):
    for email in emails:
        result = check_mails(email)
        time.sleep(6.1)