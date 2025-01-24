# Working copy of back-end logic

import csv

#read from initial database
def initial_read():

    with open("test.csv", mode="r") as database:

        catalog = csv.reader(database)

    return catalog

catalog = initial_read()

