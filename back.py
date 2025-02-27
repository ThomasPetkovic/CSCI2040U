    # Working copy of back-end logic

import csv

#read from initial database
def initial_read():

    list = []

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)

        for item in catalog:
            print(item)
            list.append(item)

    return list

list = initial_read()

#function to save modified list variable to new csv file. can be replaced with append functionality later on if optimization required.
def rewrite_csv(list):
    with open("test.csv", mode="w", newline="") as database:
        fieldnames = ["name", "description", "id"]
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow(item)

rewrite_csv(list)