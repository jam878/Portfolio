+----------------------+
| CryptoBot User Guide |
+----------------------+

=================
Table of Contents
=================
1. Requirements
	a. Python 3
	b. GDAX Module
2. GDAX Account
	a. Account Creation
	b. API Keys
	c. Account ID
	d. Payment Method
3. Running CryptoBot
	a. Script
	b. Frontend

============
Requirements
============
1. Python 3
Download the newest build of Python 3 from https://www.python.org/

2. GDAX Module
In your operating system's terminal, enter the following command 'pip install gdax'
This allows CryptoBot to communicate with the GDAX exchange servers

============
GDAX Account
============
1. Account Creation
Since CryptoBot relies on GDAX for trading, you must be a registered GDAX user
To register for GDAX, create an account on 'https://www.gdax.com/'
You will need to verify your identity using some form of ID, a picture of your face and SMS verification

2. API Keys
CryptoBot uses GDAX's API Key functionality to link to your account
In the GDAX side pane, navigate to 'API'
Take note of the string in the 'Passphrase' box
Check all three permission boxes on the top of the page
Click 'Create API Key'
Take note of the API Key and the API Secret Key
SAVE THESE IN A SECURE PLACE, THEY WILL NOT BE SHOWN AGAIN
In the included 'keys.txt' file, paste your API Keys and your passphrase in the appropriate locations
DO NOT LEAVE ANY SPACE IN BETWEEN THE COLON AND THE START OF THE KEY

3. Account ID
After pasting your API Keys and passphrase, run 'getAccountID.py'
The resulting 'AccountID.txt' file will contain your Account ID
Paste this into the appropriate space in 'keys.txt'

4. Payment Method
In the GDAX side pane, navigate to 'Settings'
In the 'Account' window in the settings, opt to update payment methods
Here you can link the bank account you will use to add funds
On the side pane, navigate to 'Accounts'
On the left window, ensure you have 'USD Account' selected
Click the small up arrow to the right of the text
Here you can transfer funds to be used by CryptoBot
Once funds are available, go back to the payment methods page and remove your bank account
FUNDS MAY TAKE A WEEK OR MORE TO BECOME AVAILABLE

=================
Running CryptoBot
=================
1. Script
To run CryptoBot, simply open 'CryptoBot.py'
If API Keys are valid, CryptoBot will begin to trade automatically

2. Frontend
To see a detailed trade history, open a terminal session in the CryptoBot folder
Run the command 'python3 -m http.server 8000'
Then navigate to '0.0.0.0:8000' in your web browser
If no transactions show but a 'transactions.txt' file is present in CryptoBot's folder, clear your cookies