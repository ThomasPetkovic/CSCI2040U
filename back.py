    # Working copy of back-end logic

import csv
from tkinter import messagebox

#read from initial database
def initial_read():

    list = []

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)

        for item in catalog:
            # print(item)
            list.append(item)

    return list

list = initial_read()

#function to save modified list variable to new csv file. can be replaced with append functionality later on if optimization required.
def rewrite_csv(list):
    with open("test.csv", mode="w", newline="") as database:
        fieldnames = ["name", "description", "id", "albumtitle", "genre", "releasedate"]  # Added new fields
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow(item)

def validate_inputs(id_, name_, description_, sample_data):
    id_ = id_.strip()
    name_ = name_.strip()
    description_ = description_.strip()
    
    if not (id_ and name_ and description_):
        messagebox.showwarning("Input Error", "Please enter ID, Name, and Description.")
        return False
    if not id_.isdigit():
        messagebox.showwarning("Input Error", "ID must be an integer.")
        return False
    if any(item["id"] == id_ for item in sample_data):  # Ensure unique ID
        messagebox.showwarning("Input Error", "ID must be unique.")
        return False
    return True

def validate_register(username, password):
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return False
    return True

def validate_login(username, password):
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return False
    return True

rewrite_csv(list)