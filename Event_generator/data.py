from faker import Faker
import csv
import random
import pandas as pd


data1 = pd.read_csv("Larnaca_out.csv")
data2 = pd.read_csv("Limassol_out.csv")
data3 = pd.read_csv("Nicosia_out.csv")
data4 = pd.read_csv("Paphos_out.csv")

# print(data1.post_code)
# print(data2.post_code)
# print(data3.post_code)
# print(data4.post_code)


print()
fake = Faker()


records=1000
print("Making %d records\n" % records)

fieldnames=['id','reason','timestamp','postal_code']
writer1 = csv.DictWriter(open("Larnaca.csv", "w",newline=''), fieldnames=fieldnames)
writer2 = csv.DictWriter(open("Limassol.csv", "w",newline=''), fieldnames=fieldnames)
writer3 = csv.DictWriter(open("Nicosia.csv", "w",newline=''), fieldnames=fieldnames)
writer4 = csv.DictWriter(open("Paphos.csv", "w",newline=''), fieldnames=fieldnames)


writer1.writerow(dict(zip(fieldnames, fieldnames)))
for i in range(0, records):
    pos=random.randint(0,len(data1.index)-1)
    writer1.writerow(dict([
    ('id', str(random.randint(1000,100000))),
    ('reason', str(random.randint(1,8))),
    ('timestamp', fake.date_time_between(start_date='-1m', end_date='now', tzinfo=None)),
    ('postal_code', str(data1.post_code[pos]))]))

writer2.writerow(dict(zip(fieldnames, fieldnames)))
for i in range(0, records):
    pos=random.randint(0,len(data2.index)-1)
    writer2.writerow(dict([
    ('id', str(random.randint(1000,100000))),
    ('reason', str(random.randint(1,8))),
    ('timestamp', fake.date_time_between(start_date='-1m', end_date='now', tzinfo=None)),
    ('postal_code', str(data2.post_code[pos]))]))


writer3.writerow(dict(zip(fieldnames, fieldnames)))
for i in range(0, records):
    pos=random.randint(0,len(data3.index)-1)
    writer3.writerow(dict([
    ('id', str(random.randint(1000,100000))),
    ('reason', str(random.randint(1,8))),
    ('timestamp', fake.date_time_between(start_date='-1m', end_date='now', tzinfo=None)),
    ('postal_code', str(data3.post_code[pos]))]))


writer4.writerow(dict(zip(fieldnames, fieldnames)))
for i in range(0, records):
    pos=random.randint(0,len(data4.index)-1)
    writer4.writerow(dict([
    ('id', str(random.randint(1000,100000))),
    ('reason', str(random.randint(1,8))),
    ('timestamp', fake.date_time_between(start_date='-1m', end_date='now', tzinfo=None)),
    ('postal_code', str(data4.post_code[pos]))]))
