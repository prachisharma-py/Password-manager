from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pword_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = web_insert.get()
    email = mail_insert.get()
    password = pword_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty.")
    else:
        try:
            with open("data.json", mode="r") as file:
                # TODO reading old data
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # TODO updating old data to new data
            data.update(new_data)
            with open("data.json", mode="w") as file:
                # TODO saving updated data
                json.dump(data, file, indent=4)
        finally:
            web_insert.delete(0, END)
            pword_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = web_insert.get()

    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No data file found!")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Not Found!", message="No details for the website exists")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

pword_label = Label(text="Password:")
pword_label.grid(column=0, row=3)

# Entries
web_insert = Entry(width=32)
web_insert.grid(column=1, row=1)
web_insert.focus()

mail_insert = Entry(width=50)
mail_insert.grid(column=1, row=2, columnspan=2)
mail_insert.insert(0, "Luna23@gmail.com")

pword_entry = Entry(width=32)
pword_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

gen_pword_button = Button(text="Generate Password", command=generate_password)
gen_pword_button.grid(column=2, row=3)

add_button = Button(text="Add", width=43, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
