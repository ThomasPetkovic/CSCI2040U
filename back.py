# Working copy of back-end logic

import csv

#read from initial database
def initial_read():

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)

        for item in catalog:
            print(item)

catalog = initial_read()