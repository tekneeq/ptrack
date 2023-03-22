import argparse
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




parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument("-t", type=str, dest="ticker", default="SPY")
parser.add_argument("--dfn", dest="dfn", default=0, type=int)
args = parser.parse_args()

day = (datetime.datetime.today() + datetime.timedelta(days=args.dfn)).strftime("%Y-%m-%d")


yesterday = None
if args.dfn == 0:
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    opts = list(opts_col.find({"expiration_date": yesterday, "data_date": {"$gt": yesterday}}))










puts = {}
calls = {}
print(f"Checking {day}")
opts = list(opts_col.find({"expiration_date": day, "data_date": {"$gt": today}}))

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


"""
puts = {
    "390": [{'open_interest': 1000, ..., }, ..., {}]

}
"""
"""
Use cases:

1) I want to know whos buying and selling options
    Are we buying more puts? more calls? in what degree
"""
highest_oi = 0
highest_oi_key = 0
sum_oi = 0
for p in pkeys:
    # p is the strike rice
    opt_list = puts[p]
    opt_list = sorted(opt_list, key=lambda d: d['data_date'])


    print(f"{p}: PUT")
    for idx, opt in enumerate(opt_list):
        print(f"\t{opt['data_date']} oi: {opt['open_interest']} volume: {opt['volume']}")

        if opt['open_interest'] > highest_oi:
            highest_oi = opt['open_interest']
            highest_oi_key = p

        # sum the latest oi
        if idx == len(opt_list) - 1:
            sum_oi += opt['open_interest']




highest_oi_c = 0
highest_oi_c_key = 0
sum_oi_c = 0
for c in ckeys:
    opt_list = calls[c]
    opt_list = sorted(opt_list, key=lambda d: d['data_date'])

    print(f"{c}: CALL")
    for idx, opt in enumerate(opt_list):
        print(f"\t{opt['data_date']} {opt['open_interest']} {opt['volume']}")

        if opt['open_interest'] > highest_oi_c:
            highest_oi_c = opt['open_interest']
            highest_oi_c_key = c

        # sum the latest oi
        if idx == len(opt_list) - 1:
            sum_oi_c += opt['open_interest']

print("Puts")
print(f"{highest_oi_key}: {highest_oi}, sum {sum_oi}")
print("Calls")
print(f"{highest_oi_c_key}: {highest_oi_c}, sum {sum_oi_c}")







