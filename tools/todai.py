import datetime

from pymongo import MongoClient
import config as config

"""
python3 todai.py
"""


client = MongoClient(host=config.HOST,
                     port=27017,
                     username=config.USER,
                     password=config.PASSWORD,
                     tls=True,
                     tlsAllowInvalidCertificates=True,
                     tlsCAFile='/home/ec2-user/ptrack/ptrack/rds-combined-ca-bundle.pem',
                     )
db = client.vesto
opts_col = db.opts

today = datetime.datetime.today().strftime("%Y-%m-%d")

puts = {}
calls = {}
opts = list(opts_col.find({"expiration_date": today, "data_date": {"$gt": today}}))

for opt in opts:
    strike_price = opt['strike_price']

    if opt['type'] == "call":
        if not strike_price in calls:
            calls[strike_price] = []

        calls[strike_price].append(opt)

    else:
        if not strike_price in puts:
            puts[strike_price] = []
        puts[strike_price].append(opt)

print(f"there are {len(calls)} call strikes and {len(puts)} put strikes")


pkeys = list(puts.keys())
pkeys.sort()

ckeys = list(calls.keys())
ckeys.sort()

for p in pkeys:
    opt_list = puts[p]
    opt_list = sorted(opt_list, key=lambda d: d['data_date'])

    print(f"{p}")
    for opt in opt_list:
        print(f"\t{opt['data_date']} {opt['open_interest']} {opt['volume']}")




for c in ckeys:
    opt_list = calls[p]
    opt_list = sorted(opt_list, key=lambda d: d['data_date'])

    print(f"{p}")
    for opt in opt_list:
        print(f"\t{opt['data_date']} {opt['open_interest']} {opt['volume']}")






