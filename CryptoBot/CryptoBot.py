# File Name:  mainScript.py
# Purpose:    Contains automatic trading algorithm and API connections
# Author:     John Morgan
# Date:       4/10/2018


import time
import datetime
import gdax
import os


# PURPOSE:  Delete any preexisting transactions.txt and data.txt files
# INPUT:    N/A
# OUTPUT:   N/A
def deleteFiles(cycleOnly):
    try:
        print("Deleting 'data.txt'...")
        os.remove("data.txt")
    except OSError as e:
        print("'data.txt' could not be found")
        print("Error:", e, "\n")
    if not cycleOnly:
        try:
            print("Deleting 'transactions.txt'...")
            os.remove("transactions.txt")
        except OSError as e:
            print("'transactions.txt' could not be found")
            print("Error:", e, "\n")


# PURPOSE:  Read API Keys, passphrase and account ID
# INPUT:    keys.txt
# OUTPUT:   Verified GDAX connection
def readKeys():
    with open("keys.txt") as key:
        keyList = list(map(str, key))
    API_KEY = keyList[0][keyList[0].find(":") + 1:keyList[0].find("\\")]
    API_SECRET = keyList[1][keyList[1].find(":") + 1:keyList[1].find("\\")]
    PASSPHRASE = keyList[2][keyList[2].find(":") + 1:keyList[2].find("\\")]
    ID = keyList[3][keyList[3].find(":") + 1:]
    client = gdax.AuthenticatedClient(API_KEY, API_SECRET, PASSPHRASE)
    return client, ID


# PURPOSE:  Get BTC 24hr trade volume
# INPUT:    N/A
# OUTPUT:   BTC 24hr trade volume
def getVolume():
    currentTicker = public_client.get_product_24hr_stats('BTC-USD')
    tradeVolume = float(currentTicker['volume'])
    return tradeVolume


# PURPOSE:  Get current price of BTC
# INPUT:    N/A
# OUTPUT:   Price of BTC/USD
def getPrice():
    currentTicker = public_client.get_product_24hr_stats('BTC-USD')
    currentPrice = float(currentTicker['last'])
    return currentPrice


# PURPOSE:  Get USD value of BTC wallet
# INPUT:    N/A
# OUTPUT:   USD Wallet funds
def getFunds():
    coinBalance = float(client.get_account(ID)['balance'])
    currentPrice = float(getPrice())
    userFunds = float(coinBalance * currentPrice)
    return userFunds


# PURPOSE:  Determines whether the current price exceeds the price ceiling or floor
# INPUT:    N/A
# OUTPUT:   A decision to buy, sell, or do nothing
def buyOrSell():
    botDecision = "No Trade"  # Bot defaults to making no action
    if userFunds > 0 and currentPrice < lastPrice - (currentPrice / 500):
        botDecision = "Buy"  # If the current price goes down significantly, the bot signals a buy
    elif userFunds > 0 and currentPrice > lastPrice + (currentPrice / 400) and coinBalance > 0:
        botDecision = "Sell"  # If the current prices goes up significantly, the bot signals a sell
    elif userFunds <= 0:
        exit()  # Script ends if the user does not have any money
    return botDecision


# PURPOSE:  Determines the amount of money to spend on a purchase or sale at any given time
# INPUT:    N/A
# OUTPUT:   Float that corresponds to amount to spend
def riskAmount():
    userFundsRisked = 0
    if 200 < userFunds < 500:  # More is at risk if the user has more money
        userFundsRisked = userFunds * 0.075
    elif 0 < userFunds <= 200:
        userFundsRisked = userFunds * 0.025
    elif userFunds >= 500:
        userFundsRisked = userFunds * 0.1
    else:
        exit()
    return userFundsRisked


# PURPOSE:  Forces script to refresh every 5 minutes
# INPUT:    N/A
# OUTPUT:   N/A
def sleep():
    if demoMode:
        time.sleep(1)
    else:
        time.sleep(120)


# PURPOSE:  Print transaction history to text document
# INPUT:    Change in Balance, Coins Bought/Sold
# OUTPUT:   transactions.txt
def printTransactions(usdBalanceDifference, coinBalanceDifference, transactionData):
    if usdBalanceDifference <= 0:
        transactionType = "Buy"
    else:
        transactionType = "Sell"
    now = str(datetime.datetime.now())
    newData = "%s,%.4f,$%.2f,%s\n" % (transactionType, coinBalanceDifference, currentPrice, now)
    if len(transactionData) >= 30:
        transactionData.pop(0)
    transactionData.append(newData)
    transactionData.reverse()
    try:
        os.remove("transactions.txt")
    except OSError as e:
        print("'transactions.txt' could not be found")
        print("Error:", e)
        print("THIS ERROR IS NORMAL WHEN STARTING CRYPTOBOT")
    with open("transactions.txt", "a") as file:
        file.write("Transaction Type,Amount,Quote,Timestamp\n")
        for i in range(0, len(transactionData)):
            file.write(transactionData[i])
        file.close()
    return transactionData


# PUPOSE:  Print routine data each cycle of the loop
# INPUT:   Bot Decision, Current Price, Trade Volume, Orders Placed, Average Price, User Budget
# OUTPUT:  data.txt
def printCycle(botDecision, currentPrice, tradeVolume, ordersPlaced, averagePrice, cycleData):
    now = str(datetime.datetime.now())
    newData = "%s,%.2f,%.2f,%d,%d,%.2f,%s\n" % (botDecision, currentPrice, averagePrice, ordersPlaced['Buy'], ordersPlaced['Sell'], tradeVolume, now)
    if len(cycleData) >= 30:
        cycleData.pop(0)
    cycleData.append(newData)
    cycleData.reverse()
    try:
        os.remove("data.txt")
    except OSError as e:
        print("'data.txt' could not be found")
        print("Error:", e)
        print("THIS ERROR IS NORMAL WHEN STARTING CRYPTOBOT\n")
    with open("data.txt", "a") as file:
        file.write("Decision,Current Price,Average Price,Buy#,Sell#,24hr Volume,Timestamp\n")
        for i in range(0, len(cycleData)):
            file.write(cycleData[i])
        file.close()
    return cycleData


deleteFiles(False)
client, ID = readKeys()
public_client = gdax.PublicClient()

# Initializes variables that will allow data compounding
ordersPlaced = {  # Track buy/sell orders
    "Buy": 0,
    "Sell": 0
}
refreshes = 0
averagePrice = 0
compundedPrice = 0
cycleData = []
transactionData = []

# Variables to be used in algorithm
currentPrice = getPrice()
lastPrice = currentPrice
userBudget = 500
# userFunds = getFunds()
userFunds = 500
coinBalance = client.get_account(ID)['balance']
tradeCooldown = 0

# Settings
volumeTrade = False
demoMode = False
ordersEnabled = False  # TODO: DO NOT ENABLE

if demoMode:
    print("SCRIPT DEMO MODE")
    time.sleep(2)

# PURPOSE:  Main loop of the program, refreshes price/wallet info every 5 minutes and directs towards buy/sell orders
# INPUT:    BTC Price, Wallet Balance
# OUTPUT:   N/A
while True:
    refreshes += 1

    # Refresh user funds
    if ordersEnabled:
        userFunds = getFunds()
    currentPrice = getPrice()

    # Ticker pull (trade volume)
    tradeVolume = getVolume()
    if refreshes == 1:
        lastVolume = tradeVolume
    if refreshes % 144 == 0:
        lastVolume = tradeVolume

    # Price pull
    currentPrice = getPrice()
    if refreshes % 20 == 0:
        lastPrice = currentPrice

    # Bot decides action and stake
    userFundsRisked = riskAmount()
    botDecision = buyOrSell()
    if tradeVolume > (lastVolume * 1.05) and coinBalance > 0:
        volumeTrade = True
        botDecision = "Sell"
    if tradeCooldown > 0:
        tradeCooldown -= 1
        botDecision = "No Trade"
    if demoMode:
        if refreshes == 1 or refreshes == 4:
            botDecision = "No Trade"
        elif refreshes == 2 or refreshes == 5:
            botDecision = "Buy"
        elif refreshes == 3 or refreshes == 6:
            botDecision = "Sell"
        elif refreshes == 7:
            exit("Finished Demo Mode")

    # Data collection
    compundedPrice += currentPrice
    averagePrice = compundedPrice / refreshes
    # If the bot decides to buy...
    if botDecision == "Buy":
        ordersPlaced["Buy"] += 1
        usdBalanceDifference = -1 * (userFundsRisked * 1.003)
        coinBalanceDifference = userFundsRisked / currentPrice
        # TODO: ENABLE BUY ORDERS
        if ordersEnabled:
            buy = client.buy(price=str(currentPrice), size=str(coinBalanceDifference), product_id='BTC-USD')
        else:
            userFunds += usdBalanceDifference
        coinBalance = float(coinBalance)
        coinBalance += coinBalanceDifference
        transactionData = printTransactions(usdBalanceDifference, coinBalanceDifference, transactionData)
        tradeCooldown = 3

    # If the bot decides to sell...
    elif botDecision == "Sell":
        ordersPlaced["Sell"] += 1
        userFundsRisked *= 0.85
        if volumeTrade:
            userFundsRisked *= 0.7
        usdBalanceDifference = userFundsRisked * 1.003
        coinBalanceDifference = -1 * (userFundsRisked / currentPrice)
        # TODO: ENABLE SELL ORDERS
        if ordersEnabled:
            sell = client.buy(price=str(currentPrice), size=str(coinBalanceDifference), product_id='BTC-USD')
        else:
            userFunds += usdBalanceDifference
        coinBalance = float(coinBalance)
        coinBalance += coinBalanceDifference
        transactionData = printTransactions(usdBalanceDifference, coinBalanceDifference, transactionData)

    # Output cycle data to data.txt
    cycleData = printCycle(botDecision, currentPrice, tradeVolume, ordersPlaced, averagePrice, cycleData)

    # Print basic data to console
    print("Last bot decision:", botDecision)
    print("Current Funds: $%.2f" % userFunds)
    print("BTC Balance:", coinBalance)
    print("Current Price: $%.2f" % currentPrice)
    print("Buy Floor: $%.2f" % (lastPrice - (currentPrice / 500)))
    print("Sell Ceiling: $%.2f\n" % (lastPrice + (currentPrice / 400)))

    sleep()
