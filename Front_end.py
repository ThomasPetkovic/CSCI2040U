from tkinter import *
from tkinter import messagebox
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

    Label(details_window, text=f"ID: id{item['id']}").pack(pady=5)
    Label(details_window, text=f"Name: {item['name']}").pack(pady=5)
    Label(details_window, text=f"Description: {item['description']}").pack(pady=5)

# Functionality of adding items
def add_item():
    add_window = Toplevel(root)
    add_window.title("Add Item")
    add_window.geometry("300x300")

    Label(add_window, text="id:").pack(pady=5)
    id_entry = Entry(add_window)
    id_entry.pack(pady=5)
    
    Label(add_window, text="name:").pack(pady=5)
    name_entry = Entry(add_window)
    name_entry.pack(pady=5)

    Label(add_window, text="description:").pack(pady=5)
    description_entry = Entry(add_window)
    description_entry.pack(pady=5)

    def save_item():
        id = id_entry.get()
        name = name_entry.get()
        description = description_entry.get()
        
        if validate_inputs(id, name, description):
            new_item = {
                "id": id,
                "name": name,
                "description": description
            }
            sample_data.append(new_item)
            refresh_listbox()
            add_window.destroy()
           
         

    Button(add_window, text="Add Item", command=save_item).pack(pady=5)

   
def validate_inputs(id, name, description):

    #remove whitespace

    id = id.strip()
    name = name.strip()
    description = description.strip()
    
    #ID Cannot have Spaces
    for spaces in range(len(id)):
        if id[spaces] == " ":
            messagebox.showwarning("Input Error", "ID cannot contain spaces.")  
            return False
    # All Fields have to be filled out
    if id == "" and name == "" and description == "":
        messagebox.showwarning("Input Error", "Please enter all fields.")
        return False
    if id == "" and  name == "":
        messagebox.showwarning("Input Error", "Please enter ID and Name.")
        return False
    if id == "" and description == "":
        messagebox.showwarning("Input Error", "Please enter ID and Description.")
        return False
    if name == "" and description == "":
        messagebox.showwarning("Input Error", "Please enter Name and Description.")
        return False
    if id == "":
        messagebox.showwarning("Input Error", "Please enter ID.")
        return False
    if name == "":
        messagebox.showwarning("Input Error", "Please enter Name.")
        return False
    if description == "":
        messagebox.showwarning("Input Error", "Please enter Description.")
        return False
    
    # Id must be an integer
    if not id.isdigit():
        messagebox.showwarning("Input Error", "ID must be an integer.")
        return False
    
    # ID must be unique
    for item in sample_data:
        if item["id"] == id:
            messagebox.showwarning("Input Error", "ID must be unique.")
            return False
    return True
 

def edit_item():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Error", "Please select an item to edit.")
        return

    item = sample_data[selected_index[0]]

    edit_window = Toplevel(root)
    edit_window.title("Edit Item")
    edit_window.geometry("300x300")

    Label(edit_window, text="id:").pack(pady=5)
    id_entry = Entry(edit_window)
    id_entry.insert(0, item["id"])
    id_entry.pack(pady=5)
    
    Label(edit_window, text="name:").pack(pady=5)
    name_entry = Entry(edit_window)
    name_entry.insert(0, item["name"])
    name_entry.pack(pady=5)

    Label(edit_window, text="description:").pack(pady=5)
    description_entry = Entry(edit_window)
    description_entry.insert(0, item["description"])
    description_entry.pack(pady=5)

    def save_item():
        new_id = id_entry.get()
        new_name = name_entry.get()
        new_description = description_entry.get()

        if validate_inputs(new_id, new_name, new_description):
            item["id"] = new_id
            item["name"] = new_name
            item["description"] = new_description
            refresh_listbox()
            edit_window.destroy()

    Button(edit_window, text="Save Changes", command=save_item).pack(pady=5)

# Function to edit an existing item (placeholder, does nothing

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
