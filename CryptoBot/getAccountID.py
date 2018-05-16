# File Name:  getAccountID.py
# Purpose:    Get BTC wallet ID for GDAX trading
# Author:     John Morgan
# Date:       5/14/18

import gdax
import os
import time

def sleep(sleepTime):
    time.sleep(sleepTime)

# Delete 'AccountID.txt' if it exists
try:
    os.remove("AccountID.txt")
except OSError as e:
    print("No 'AccountID.txt' found...")
    sleep(1)
    print("Fetching your ID...")
    sleep(2)

# Read API Keys and account ID from keys.txt
with open("keys.txt") as key:
    keyList = list(map(str, key))
API_KEY = keyList[0][keyList[0].find(":") + 1:keyList[0].find("\\")]
API_SECRET = keyList[1][keyList[1].find(":") + 1:keyList[1].find("\\")]
PASSPHRASE = keyList[2][keyList[2].find(":") + 1:keyList[2].find("\\")]
client = gdax.AuthenticatedClient(API_KEY, API_SECRET, PASSPHRASE)

accountID = client.get_accounts()
accountID = accountID[0]['id']
with open("AccountID.txt", "a") as file:
    file.write("This is your BTC Wallet account ID\n")
    file.write("Paste this value next to the 'ACCOUNT:' section in keys.txt\n")
    file.write(accountID)

print("Your GDAX Account ID is available in 'AccountID.txt'")
