from tkinter import *
from tkinter import messagebox,ttk
import customtkinter as ctk
import back
from tkinter import filedialog
from PIL import Image, ImageTk
import os

#colors

peach = "#FFE5B4"
dark_peach = "#FFE5D9"
light_peach = "#FDEEEB"
maroon = "#800000"
dark_maroon = "#6B0F1A"
light_maroon = "#FAD4C0"
text = "#4B0A12"
brown = "#8f4535"
hover_maroon = "#9A1B1F"

# Current user dictionary to store username and permission
current_user = {
    "username": None,
    "permission": None
}


# Appearance

ctk.set_appearance_mode(maroon)
ctk.set_default_color_theme("blue") #temporary

# Check if running in pytest
if "PYTEST_CURRENT_TEST" in os.environ:
    # Prevent GUI from launching during tests
    exit()

# Check if running in GitHub Actions
GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

if GITHUB_ACTIONS:
    import tkinter
    tkinter.Tk().withdraw()  # Prevent GUI from launching


def admin_login():
    return current_user["username"] == "admin" and current_user["permission"] == "admin"

def user_login():
    if not admin_login():
        messagebox.showwarning("Error", "You are not logged in as admin.")
        return False
    return True
       

def load_data_from_csv():
    return back.initial_read()

sample_data = load_data_from_csv()

def show_item_details(item):

    details_window = ctk.CTkToplevel(root)
    details_window.title("Item Details")
    details_window.geometry("300x400")
    ctk.CTkLabel(details_window, text=f"ID: {item['id']}", text_color=peach).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Name: {item['name']}",text_color=peach).pack(pady=5)
    ctk.CTkLabel(details_window, text=f"Description: {item['description']}",text_color=peach).pack(pady=5)
    
    ctk.CTkLabel(details_window, text=f"Image: {item.get('albumtitle','')}",text_color=peach).pack(pady=5)
    ctk.CTkButton(details_window, text="Preview Lyrics", command = lambda: preview_lyrics(item),fg_color=maroon,hover_color=dark_maroon).pack(pady=5)

    image_display = ctk.CTkLabel(details_window,text="")
    image_display.pack(pady=5)

    def load_image(path):
        try:
            img = Image.open(path)
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            image_display.configure(image=photo)
            image_display.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Error : {e}")

    if "image_path" in item and item["image_path"]:
        load_image(item["image_path"])

    
    def upload_image():
        if not user_login():
            return
        messagebox.showinfo("Uploading Image", "Admin is uploading image")
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.img")]
        )
        if path:
            item["image_path"] = path
            load_image(path)

    ctk.CTkButton(details_window, text="Upload Image", command=upload_image,fg_color=maroon, hover_color=hover_maroon).pack(pady=5)

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

    register_window = ctk.CTkToplevel(root)
    register_window.title("Register")
    register_window.geometry("300x300")
    ctk.CTkLabel(register_window, text="Username:", text_color=peach).pack(pady=5)
    username_entry = ctk.CTkEntry(register_window)
    username_entry.pack(pady=5)
    ctk.CTkLabel(register_window, text="Password:", text_color=peach).pack(pady=5)
    password_entry = ctk.CTkEntry(register_window, show="*")
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

    ctk.CTkButton(register_window, text="Register", command=save_register, fg_color=maroon,hover_color=hover_maroon).pack(pady=5)


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

    login_window = ctk.CTkToplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")
    ctk.CTkLabel(login_window, text="Username:",text_color=peach).pack(pady=5)
    username_entry = ctk.CTkEntry(login_window)
    username_entry.pack(pady=5)
    ctk.CTkLabel(login_window, text="Password:",text_color=peach).pack(pady=5)
    password_entry = ctk.CTkEntry(login_window, show="*")


    password_entry.pack(pady=5)
    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "admin":
            permission = "admin"
        else:
            permission = "user"

        current_user["username"] = username
        current_user["permission"] = permission

    
        messagebox.showinfo("Success", f"Login Successful as {permission}")
        display_username(username, permission)
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

    ctk.CTkButton(login_window, text="Login", command=check_login, fg_color=maroon, hover_color=hover_maroon).pack(pady=5)


def validate_login(username, password):
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return False
    return True

def display_username(username, permission):
    global username_label
    if 'username_label' in globals():
        username_label.destroy()

    username_label = ctk.CTkLabel(root, text=f"{username} ({permission})", text_color=maroon)

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

        
        refresh_tree()

def logout():
    global username_label
    if 'username_label' in globals():
        username_label.destroy()
    
    current_user["username"] = None
    current_user["permission"] = None

    messagebox.showinfo("Success", "Logout Successful")
   
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

        
        if item.get("releasedate","").lower().startswith(entry):
            found.append(item)

        if item.get("albumtitle","").lower().startswith(entry):
            found.append(item)
        
        if item.get("genre","").lower().startswith(entry):
            found.append(item)

        if item.get("description","").lower().startswith(entry):
            found.append(item)
        
        if item["id"].lower().startswith(entry):
            found
        

    if not found:
        messagebox.showerror("ERROR", "No matching search results.")
        refresh_tree()
    else:
        for it in found:
            tree.insert("", "end", values=(it["name"], it.get("releasedate",""), it.get("albumtitle","")))


def preview_lyrics(item):
    preview_window = ctk.CTkToplevel(root)
    preview_window.title("Lyrics Preview")
    preview_window.geometry("400x500")
    preview_window.resizable(True, True)  # Allow the user to resize

    # 1. Fetch lyrics as a list of lines
    lyrics_list = back.get_lyrics(item)
    # 2. Join into a single string
    lyrics_text = "\n".join(lyrics_list)

    # 3. Create a read-only textbox that fills/resizes with the window
    text_widget = ctk.CTkTextbox(preview_window, text_color=peach, wrap="word")  
    text_widget.insert("1.0", lyrics_text)
    text_widget.configure(state="disabled")
    text_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)



def add_item():
    add_window = ctk.CTkToplevel(root)
    add_window.title("Add Item")
    add_window.geometry("400x500")
    ctk.CTkLabel(add_window, text="ID:",text_color=peach).pack(pady=5)
    id_entry = ctk.CTkEntry(add_window)
    id_entry.pack(pady=5)
    ctk.CTkLabel(add_window, text="Name:",text_color=peach).pack(pady=5)
    name_entry = ctk.CTkEntry(add_window)
    name_entry.pack(pady=5)
    ctk.CTkLabel(add_window, text="Description:",text_color=peach).pack(pady=5)
    description_entry = ctk.CTkEntry(add_window)
    description_entry.pack(pady=5)
    ctk.CTkLabel(add_window, text="Album Title:",text_color=peach).pack(pady=5)
    album_title_entry = ctk.CTkEntry(add_window)
    album_title_entry.pack(pady=5)
    ctk.CTkLabel(add_window, text="Genre:",text_color=peach).pack(pady=5)
    genre_entry = ctk.CTkEntry(add_window)
    genre_entry.pack(pady=5)
    ctk.CTkLabel(add_window, text="Release Date:",text_color=peach).pack(pady=5)
    release_date_entry = ctk.CTkEntry(add_window)

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

    ctk.CTkButton(add_window, text="Add Item", command=save_item,fg_color=maroon, hover_color=hover_maroon).pack(pady=5)

def validate_inputs(id_, name_, description_):

    if not (id_ and name_ and description_):
        messagebox.showwarning("Input Error", "Please enter ID, Name, and Description.")
        return False
    if not id_.isdigit():
        messagebox.showwarning("Input Error", "ID must be an integer.")
        return False

    for item in sample_data:
        if item["id"] == id_:
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

    edit_window = ctk.CTkToplevel(root)
    edit_window.title("Edit Item")
    edit_window.geometry("400x500")
    ctk.CTkLabel(edit_window, text="ID:",text_color=peach).pack(pady=5)
    id_entry = ctk.CTkEntry(edit_window)
    id_entry.insert(0, item["id"])
    id_entry.pack(pady=5)
    ctk.CTkLabel(edit_window, text="Name:",text_color=peach).pack(pady=5)
    name_entry = ctk.CTkEntry(edit_window)
    name_entry.insert(0, item["name"])
    name_entry.pack(pady=5)
    ctk.CTkLabel(edit_window, text="Description:",text_color=peach).pack(pady=5)
    description_entry = ctk.CTkEntry(edit_window)
    description_entry.insert(0, item["description"])
    description_entry.pack(pady=5)
    ctk.CTkLabel(edit_window, text="Album Title:",text_color=peach).pack(pady=5)
    album_title_entry = ctk.CTkEntry(edit_window)
    album_title_entry.insert(0, item.get("albumtitle",""))
    album_title_entry.pack(pady=5)
    ctk.CTkLabel(edit_window, text="Genre:",text_color=peach).pack(pady=5)
    genre_entry = ctk.CTkEntry(edit_window)
    genre_entry.insert(0, item.get("genre",""))
    genre_entry.pack(pady=5)
    ctk.CTkLabel(edit_window, text="Release Date:",text_color=peach).pack(pady=5)
    release_date_entry = ctk.CTkEntry(edit_window)

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

    ctk.CTkButton(edit_window, text="Save Changes", command=save_changes,fg_color=maroon, hover_color=hover_maroon).pack(pady=5)

def delete_item():
    if not user_login():
        return
    messagebox.showinfo("Deleting Item", "Admin is deleting item")
    
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

            file.write(f"{item['id']},{item['name']},{item['description']},{item.get('albumtitle','')},{item.get('genre','')},{item.get('releasedate','')},{item.get('image_path','')}\n")
            

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

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Catalog Management System")
    root.geometry("1300x700")
    root.configure(fg_color=light_maroon, bg_color=peach) 



    search_frame = ctk.CTkFrame(root)
    search_frame.pack(side=TOP, padx=10, pady=5)

    root.lower()
    root.attributes("-topmost", False)


    search_entry = ctk.CTkEntry(search_frame, width=130)
    search_entry.insert(0, "Search for an item...")
    search_entry.pack(side=LEFT)

    search_button = ctk.CTkButton(search_frame, text="Search 🔍", command=search_item, fg_color=maroon,bg_color=peach, hover_color=brown)
    def clear_placeholder(event):
        if search_entry.get() == "Search for an item...":
            search_entry.delete(0, END)

    search_entry.bind("<FocusIn>", clear_placeholder)


    search_button = ctk.CTkButton(search_frame, text="Search", command=search_item, fg_color=maroon,bg_color=peach, hover_color=dark_maroon)
    search_button.pack(side=LEFT, padx=0)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview", foreground="black", background=peach, rowheight=25, fieldbackground=peach)
    style.configure("Treeview.Heading", background=brown, foreground=peach, relief="flat")
    style.map("Treeview", background=[("selected", maroon)], foreground=[("selected", peach)])
    style.map("Treeview.Heading", background=[("pressed", maroon)], foreground=[("pressed", peach)])


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


    ctk.CTkButton(root, text="View Details 👁️", command=view_details,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Add Item ➕ ", command=add_item,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Edit Item ✏️", command=edit_item,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Delete Item 🗑️", command=delete_item,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Register 📝", command=register,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Login 🔓", command=login,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)
    ctk.CTkButton(root, text="Logout 🔒", command=logout,fg_color=maroon, hover_color=hover_maroon).pack(side=LEFT, padx=10, pady=10)


    refresh_tree()
    root.mainloop()

