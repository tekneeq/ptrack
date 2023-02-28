import argparse
import datetime

import instance.config as Config

import pymongo
from pymongo import MongoClient
import pprint

from pytz import timezone

def valid_date(s):
    """

    return strings
    """
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date().strftime('%Y-%m-%d')
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

client = MongoClient(host=Config.HOST,
                     port=27017,
                     username=Config.USER,
                     password=Config.PASSWORD,
                     tls=True,
                     tlsAllowInvalidCertificates=True,
                     tlsCAFile='/home/ec2-user/ptrack/ptrack/rds-combined-ca-bundle.pem',
                     )
db = client.vesto
vesto_col = db.vesto
opt_col = db.opts

pp = pprint.PrettyPrinter(width=41, compact=True)

tz = timezone('EST')


parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)


parser.add_argument(
    "-d", help="format YYYY-MM-DD", dest="expdate", default=datetime.datetime.now(tz).strftime('%Y-%m-%d'), type=valid_date
)

args = parser.parse_args()

# y = mx + b
def get_slope(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return (m, b)


expdate = args.expdate
print(f'Grabbing isect, ptop, ctop for {expdate}')
data = vesto_col.find({'exp_date': f'{expdate}'}).sort('data_date', pymongo.DESCENDING)

"""
{
    "_id": ObjectId("63fe1f00bffc59a966d74090"),
    "intersection": [397.15, 36125.01],
    "ptop": [417.0, 391656.3099999999],
    "pbot": [378.0, 11.11],
    "ctop": [378.0, 99944.35999999999],
    "cbot": [417.0, 63.36],
    "data_date": "2023-02-28T10:34:24",
    "exp_date": "2023-02-28",
    "version": 1,
}
"""
for d in data:
    newdict = {}
    newdict['isect'] = d['intersection'][0]
    newdict['ctop'] = d['ctop'][1]
    newdict['ptop'] = d['ptop'][1]
    newdict['date_collected'] = d['data_date']
