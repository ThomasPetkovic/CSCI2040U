from tkinter import *
from tkinter import messagebox, ttk
import back
import os

# Check if running in GitHub Actions
GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

if GITHUB_ACTIONS:
    import tkinter
    tkinter.Tk().withdraw()  # Prevent GUI from launching


def load_data_from_csv():
    return back.initial_read()

sample_data = load_data_from_csv()

def show_item_details(item):
    details_window = Toplevel(root)
    details_window.title("Item Details")
    details_window.geometry("300x200")
    Label(details_window, text=f"ID: {item['id']}").pack(pady=5)
    Label(details_window, text=f"Name: {item['name']}").pack(pady=5)
    Label(details_window, text=f"Description: {item['description']}").pack(pady=5)

def view_details():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select an item to view details.")
        return
    row_values = tree.item(selected[0], "values")
    selected_name = row_values[0]
    selected_date = row_values[1]
    selected_album = row_values[2]
    found_item = None
    for it in sample_data:
        if (
            it["name"] == selected_name
            and it.get("releasedate", "") == selected_date
            and it.get("albumtitle", "") == selected_album
        ):
            found_item = it
            break
    if not found_item:
        messagebox.showwarning("Error", "Item not found in sample_data.")
    else:
        show_item_details(found_item)

def register():
    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x300")
    Label(register_window, text="Username:").pack(pady=5)
    username_entry = Entry(register_window)
    username_entry.pack(pady=5)
    Label(register_window, text="Password:").pack(pady=5)
    password_entry = Entry(register_window, show="*")
    password_entry.pack(pady=5)
    def save_register():
        username = username_entry.get()
        password = password_entry.get()
        if validate_register(username, password):
            if not is_username_taken(username):
                with open("register.csv", "a", newline='') as file:
                    file.write(f"{username},{password}\n")
                register_window.destroy()
                messagebox.showinfo("Success", "Registration Successful")
            else:
                messagebox.showwarning("Error", "Username already exists")
    Button(register_window, text="Register", command=save_register).pack(pady=5)

def validate_register(username, password):
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return False
    return True

def is_username_taken(username):
    try:
        with open("register.csv", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    registered_username, _ = parts
                    if registered_username == username:
                        return True
    except FileNotFoundError:
        pass
    return False

def login():
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")
    Label(login_window, text="Username:").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)
    Label(login_window, text="Password:").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)
    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_login(username, password):
            try:
                with open("register.csv", "r") as file:
                    for line in file:
                        line = line.strip()
                        if line == f"{username},{password}":
                            login_window.destroy()
                            messagebox.showinfo("Success", "Login Successful")
                            display_username(username)
                            load_user_data(username)
                            return
                messagebox.showwarning("Error", "Invalid username or password")
            except FileNotFoundError:
                messagebox.showwarning("Error", "No users registered yet.")
    Button(login_window, text="Login", command=check_login).pack(pady=5)

def validate_login(username, password):
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return False
    return True

def display_username(username):
    global username_label
    if 'username_label' in globals():
        username_label.destroy()
    username_label = Label(root, text=username)
    username_label.pack(side=RIGHT, padx=10, pady=10)

def load_user_data(username):
    global sample_data
    try:
        with open(f"{username}_data.csv", "r") as file:
            sample_data = []
            for line in file:
                id_, name_, desc_ = line.strip().split(',')
                sample_data.append({"id": id_, "name": name_, "description": desc_})
        refresh_tree()
    except FileNotFoundError:
        sample_data = []
        refresh_tree()

def logout():
    logout_window = Toplevel(root)
    logout_window.title("Logout")
    logout_window.geometry("300x300")
    Label(logout_window, text="Are you sure you want to logout?").pack(pady=5)
    def confirm_logout():
        global sample_data
        logout_window.destroy()
        if 'username_label' in globals() and username_label:
            username_label.destroy()
        messagebox.showinfo("Success", "Logout Successful")
        sample_data = []
        refresh_tree()
    Button(logout_window, text="Yes", command=confirm_logout).pack(pady=5)
    Button(logout_window, text="No", command=logout_window.destroy).pack(pady=5)

def search_item():
    entry = search_entry.get().strip().lower()
    if not entry:
        refresh_tree()
        return
    for child in tree.get_children():
        tree.delete(child)
    found = []
    for item in sample_data:
        if item["name"].lower().startswith(entry):
            found.append(item)
    print(found)
    if not found:
        messagebox.showerror("ERROR", "No matching search results.")
        refresh_tree()
    else:
        for it in found:
            tree.insert("", "end", values=(it["name"], it.get("releasedate",""), it.get("albumtitle","")))

def add_item():
    add_window = Toplevel(root)
    add_window.title("Add Item")
    add_window.geometry("400x500")
    Label(add_window, text="ID:").pack(pady=5)
    id_entry = Entry(add_window)
    id_entry.pack(pady=5)
    Label(add_window, text="Name:").pack(pady=5)
    name_entry = Entry(add_window)
    name_entry.pack(pady=5)
    Label(add_window, text="Description:").pack(pady=5)
    description_entry = Entry(add_window)
    description_entry.pack(pady=5)
    Label(add_window, text="Album Title:").pack(pady=5)
    album_title_entry = Entry(add_window)
    album_title_entry.pack(pady=5)
    Label(add_window, text="Genre:").pack(pady=5)
    genre_entry = Entry(add_window)
    genre_entry.pack(pady=5)
    Label(add_window, text="Release Date:").pack(pady=5)
    release_date_entry = Entry(add_window)
    release_date_entry.pack(pady=5)
    def save_item():
        id_ = id_entry.get().strip()
        name_ = name_entry.get().strip()
        desc_ = description_entry.get().strip()
        albumtitle = album_title_entry.get().strip()
        genre = genre_entry.get().strip()
        releasedate = release_date_entry.get().strip()
        if validate_inputs(id_, name_, desc_):
            new_item = {
                "id": id_,
                "name": name_,
                "description": desc_,
                "albumtitle": albumtitle,
                "genre": genre,
                "releasedate": releasedate
            }
            sample_data.append(new_item)
            refresh_tree()
            add_window.destroy()
            save_user_data()
    Button(add_window, text="Add Item", command=save_item).pack(pady=5)

def validate_inputs(id_, name_, description_):
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

def edit_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select an item to edit.")
        return
    row_values = tree.item(selected[0], "values")
    selected_name = row_values[0]
    selected_date = row_values[1]
    selected_album = row_values[2]
    item = None
    for d in sample_data:
        if d["name"] == selected_name and d.get("releasedate","") == selected_date and d.get("albumtitle","") == selected_album:
            item = d
            break
    if not item:
        messagebox.showwarning("Error", "Item not found.")
        return
    edit_window = Toplevel(root)
    edit_window.title("Edit Item")
    edit_window.geometry("400x500")
    Label(edit_window, text="ID:").pack(pady=5)
    id_entry = Entry(edit_window)
    id_entry.insert(0, item["id"])
    id_entry.pack(pady=5)
    Label(edit_window, text="Name:").pack(pady=5)
    name_entry = Entry(edit_window)
    name_entry.insert(0, item["name"])
    name_entry.pack(pady=5)
    Label(edit_window, text="Description:").pack(pady=5)
    description_entry = Entry(edit_window)
    description_entry.insert(0, item["description"])
    description_entry.pack(pady=5)
    Label(edit_window, text="Album Title:").pack(pady=5)
    album_title_entry = Entry(edit_window)
    album_title_entry.insert(0, item.get("albumtitle",""))
    album_title_entry.pack(pady=5)
    Label(edit_window, text="Genre:").pack(pady=5)
    genre_entry = Entry(edit_window)
    genre_entry.insert(0, item.get("genre",""))
    genre_entry.pack(pady=5)
    Label(edit_window, text="Release Date:").pack(pady=5)
    release_date_entry = Entry(edit_window)
    release_date_entry.insert(0, item.get("releasedate",""))
    release_date_entry.pack(pady=5)
    def save_changes():
        new_id = id_entry.get().strip()
        new_name = name_entry.get().strip()
        new_desc = description_entry.get().strip()
        new_albumtitle = album_title_entry.get().strip()
        new_genre = genre_entry.get().strip()
        new_releasedate = release_date_entry.get().strip()
        if validate_inputs(new_id, new_name, new_desc):
            item["id"] = new_id
            item["name"] = new_name
            item["description"] = new_desc
            item["albumtitle"] = new_albumtitle
            item["genre"] = new_genre
            item["releasedate"] = new_releasedate
            refresh_tree()
            edit_window.destroy()
            save_user_data()
    Button(edit_window, text="Save Changes", command=save_changes).pack(pady=5)

def delete_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select an item to delete.")
        return
    row_values = tree.item(selected[0], "values")
    selected_name = row_values[0]
    selected_date = row_values[1]
    selected_album = row_values[2]
    to_delete = None
    for d in sample_data:
        if d["name"] == selected_name and d.get("releasedate","") == selected_date and d.get("albumtitle","") == selected_album:
            to_delete = d
            break
    if to_delete:
        sample_data.remove(to_delete)
        refresh_tree()
        save_user_data()
    else:
        messagebox.showwarning("Error", "Item not found.")

def save_user_data():
    username = username_label.cget("text") if 'username_label' in globals() else "default_user"
    with open(f"{username}_data.csv", "w", newline='') as file:
        for item in sample_data:
            file.write(f"{item['id']},{item['name']},{item['description']}\n")

ascending_name = True
ascending_date = True
ascending_album = True

def on_name_click():
    global ascending_name
    sample_data.sort(key=lambda x: x["name"].lower(), reverse=(not ascending_name))
    ascending_name = not ascending_name
    refresh_tree()

def on_date_click():
    global ascending_date
    sample_data.sort(key=lambda x: x.get("releasedate",""), reverse=(not ascending_date))
    ascending_date = not ascending_date
    refresh_tree()

def on_album_click():
    global ascending_album
    sample_data.sort(key=lambda x: x.get("albumtitle","").lower(), reverse=(not ascending_album))
    ascending_album = not ascending_album
    refresh_tree()

def refresh_tree():
    for child in tree.get_children():
        tree.delete(child)
    for item in sample_data:
        tree.insert("", "end", values=(item["name"], item.get("releasedate",""), item.get("albumtitle","")))
    back.rewrite_csv(sample_data)

def lyrical_preview():
    return "Nah, I'm good."


root = Tk()
root.title("Catalog Management System")
root.geometry("900x600")

search_frame = Frame(root)
search_frame.pack(side=TOP, padx=10, pady=5)

search_entry = Entry(search_frame, width=130)
search_entry.insert(0, "Search for an item...")
search_entry.pack(side=LEFT)

search_button = Button(search_frame, text="Search", command=search_item)
search_button.pack(side=LEFT, padx=5)

tree = ttk.Treeview(root, columns=("Name","Date","Album"), show="headings")
tree.heading("Name", text="Name", command=on_name_click)
tree.heading("Date", text="Date", command=on_date_click)
tree.heading("Album", text="Album", command=on_album_click)
tree.column("Name", width=200)
tree.column("Date", width=120)
tree.column("Album", width=180)
tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Hover functionality to show a tipbox when hovering over an item
tipbox = None

def show_tipbox(event):
    global tipbox
    if tipbox:
        tipbox.destroy()
    item = tree.identify_row(event.y)
    if item:
        row_values = tree.item(item, "values")
        if row_values:
            tipbox = Toplevel(root)
            tipbox.geometry("300x100")
            tipbox.overrideredirect(True)
            tipbox.wm_attributes("-topmost", 1)
            Label(tipbox, text=f"Name: {row_values[0]}\nDate: {row_values[1]}\nAlbum: {row_values[2]}").pack(pady=5)
            tipbox.geometry(f"+{event.x_root+2}+{event.y_root+2}")
            tipbox.after(2000, tipbox.destroy)

tree.bind("<Motion>", show_tipbox)

Button(root, text="View Details", command=view_details).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Add Item", command=add_item).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Edit Item", command=edit_item).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Delete Item", command=delete_item).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Register", command=register).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Login", command=login).pack(side=LEFT, padx=10, pady=10)
Button(root, text="Logout", command=logout).pack(side=LEFT, padx=10, pady=10)

refresh_tree()
if __name__ == "__main__":
    root.mainloop()
