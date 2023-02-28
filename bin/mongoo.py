import .instance.config as Config

import pymongo
from pymongo import MongoClient

client = MongoClient(host=Config.host,
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

# y = mx + b
def get_slope (x1, y1, x2, y2):
    m = (y2-y1)/ (x2-x1)
    b = y1 - m*x1

    return (m,b)


expdate = '2023-02-28'
data = list(vesto_col.find({f'exp_date: {expdate}'}))

for d in data:
    print(d)
