from tkinter import *
from tkinter import messagebox
import csv
import back

# Function to load data from CSV file
def load_data_from_csv():
    return back.initial_read()

# Load initial data from CSV
sample_data = load_data_from_csv()

# Function to display item details
def show_item_details(item):
    details_window = Toplevel(root)
    details_window.title("Item Details")
    details_window.geometry("300x200")

    Label(details_window, text=f"ID: {item['ID']}").pack(pady=5)
    Label(details_window, text=f"Name: {item['Name']}").pack(pady=5)
    Label(details_window, text=f"Description: {item['Description']}").pack(pady=5)

# Function to add a new item (placeholder, does nothing)
def add_item():
    messagebox.showinfo("Info", "Add Item functionality will be implemented later.")

# Function to edit an existing item (placeholder, does nothing)
def edit_item():
    messagebox.showinfo("Info", "Edit Item functionality will be implemented later.")

# Function to refresh the listbox
def refresh_listbox():
    listbox.delete(0, END)
    for item in sample_data:
        listbox.insert(END, item["name"])

# Main application window
root = Tk()
root.title("Catalog Management System")
root.geometry("400x300")

# Listbox to display catalog items
listbox = Listbox(root)
listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Populate listbox with data from CSV
refresh_listbox()

# Button to view item details
def view_details():
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = sample_data[selected_index[0]]
        show_item_details(selected_item)
    else:
        messagebox.showwarning("Error", "Please select an item to view details.")

Button(root, text="View Details", command=view_details).pack(side=LEFT, padx=10, pady=10)

# Button to add a new item (placeholder)
Button(root, text="Add Item", command=add_item).pack(side=LEFT, padx=10, pady=10)

# Button to edit an existing item (placeholder)
Button(root, text="Edit Item", command=edit_item).pack(side=LEFT, padx=10, pady=10)

# Run the application
root.mainloop()