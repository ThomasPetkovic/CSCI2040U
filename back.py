# Working copy of back-end logic

import csv

#read from initial database
def initial_read():

    data_list = []

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)

        for item in catalog:
            print(item)
            data_list.append(item)

    return data_list

data_list = initial_read()

#function to save modified list variable to new csv file. can be replaced with append functionality later on if optimization required.
def rewrite_csv(data_list):
    with open("test.csv", mode="w", newline="") as database:
        fieldnames = ["name", "description", "id"]
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for item in data_list:
            writer.writerow(item)

rewrite_csv(data_list)