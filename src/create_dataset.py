import pandas as pd
import random
from datetime import datetime, timedelta


wallets = [
    "WALLET001",
    "WALLET002",
    "WALLET003",
    "WALLET004",
    "WALLET005"
]


countries = [
    "USA",
    "UK",
    "Pakistan",
    "Germany",
    "Russia"
]


merchants = [
    "Binance",
    "Coinbase",
    "Kraken"
]


transactions = []


for i in range(1000):

    wallet = random.choice(wallets)

    amount = random.randint(10,5000)


    # create suspicious transactions
    if random.random() < 0.05:

        amount = random.randint(50000,200000)


    date = datetime.now() - timedelta(
        days=random.randint(1,365)
    )


    transactions.append({

        "transaction_id":f"TX{i}",

        "wallet_id":wallet,

        "amount":amount,

        "timestamp":date,

        "country":random.choice(countries),

        "merchant":random.choice(merchants),

        "wallet_age_days":
        random.randint(1,1000),

        "previous_transactions":
        random.randint(0,500)

    })


df=pd.DataFrame(transactions)


df.to_csv(
"data/raw/transactions.csv",
index=False
)


print("Dataset Created")
