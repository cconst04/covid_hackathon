from faker import Faker
import csv
import random
import pandas as pd


#data = pd.read_csv("Larnaca_out.csv")
#data = pd.read_csv("Limassol_out.csv")
#data = pd.read_csv("Nicosia_out.csv")
data = pd.read_csv("Paphos.csv")

print(data.post_code)

fake = Faker()


records=1000
print("Making %d records\n" % records)

fieldnames=['id','reason','timestamp','postal_code']
writer = csv.DictWriter(open("Paphos.csv", "w",newline=''), fieldnames=fieldnames)

writer.writerow(dict(zip(fieldnames, fieldnames)))
for i in range(0, records):
    pos=random.randint(0,24)
    writer.writerow(dict([
    ('id', str(random.randint(1000,100000))),
    ('reason', str(random.randint(1,8))),
    ('timestamp', fake.date_time_between(start_date='-30y', end_date='now', tzinfo=None)),
    ('postal_code', str(data.post_code[pos]))]))
