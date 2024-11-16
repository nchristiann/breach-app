import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests

EMAILS_FILE = "./emails.txt"
HIBP_API_KEY = "ab62cea28a114653909fa9ef1547d590"
BASE_URL = "https://haveibeenpwned.com/api/v3"

def load_emails():
    try:
        with open(EMAILS_FILE, "r") as file:
            emails = file.readlines()
            for email in emails:
                email_listbox.insert(tk.END, email.strip())
    except FileNotFoundError:
        pass

def save_emails():
    emails = email_listbox.get(0, tk.END)
    with open(EMAILS_FILE, "w") as file:
        for email in emails:
            file.write(email + "\n")

def check_breach(email):
    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "user-agent": "PythonApp"
    }
    response = requests.get(f"{BASE_URL}/breachedaccount/{email}", headers=headers)
    if response.status_code == 200:
        return f"{email}: Breached! Details: {response.json()}"
    elif response.status_code == 404:
        return f"{email}: No breach found."
    else:
        return f"{email}: Error {response.status_code} - {response.text}"

def add_email(event=None):  # event parameter is added for the keybind
    email = email_entry.get().strip()
    if email and email not in email_listbox.get(0, tk.END):
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
        save_emails()
    else:
        messagebox.showwarning("Invalid Email", "Enter a valid email or avoid duplicates.")

def delete_email():
    selected_email = email_listbox.curselection()
    if selected_email:
        email_listbox.delete(selected_email)
        save_emails()
    else:
        messagebox.showwarning("No Selection", "Select an email to delete.")

def check_all_emails():
    emails = email_listbox.get(0, tk.END)
    if not emails:
        messagebox.showinfo("No Emails", "Add some emails first.")
        return

    results_text.delete(1.0, tk.END)
    for email in emails:
        result = check_breach(email)
        results_text.insert(tk.END, result + "\n")

root = tk.Tk()
root.title("Email Breach Checker")
root.geometry("800x600")
root.resizable(False, False)

# Set a modern look using colors, fonts, and padding
root.configure(bg="#2c3e50")

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background='#34495e')
style.configure('TLabel', background='#34495e', foreground='white', font=('Helvetica', 12))
style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 12, 'bold'), padding=10)
style.configure('TEntry', font=('Helvetica', 12), padding=10)
style.configure('TListbox', font=('Helvetica', 12), background='#ecf0f1')

input_frame = ttk.Frame(root, padding="20 20 20 20")
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Label for email input
email_label = ttk.Label(input_frame, text="Enter Email:")
email_label.pack(pady=10)

# Entry for email input
email_entry = ttk.Entry(input_frame, width=30)
email_entry.pack(fill=tk.X, expand=True, pady=5)

# Bind Enter key to the add_email function
email_entry.bind("<Return>", add_email)

# Delete Email button
delete_button = ttk.Button(input_frame, text="Delete Email", command=delete_email)
delete_button.pack(pady=10, fill=tk.X)

# Listbox to show emails
email_listbox = tk.Listbox(input_frame, font=('Helvetica', 12), height=8)
email_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

# Button to check breaches
check_button = ttk.Button(input_frame, text="Check Breaches", command=check_all_emails)
check_button.pack(pady=10, fill=tk.X)

# Results Textbox to display breach results
results_text = tk.Text(input_frame, font=('Helvetica', 12), height=10, wrap=tk.WORD)
results_text.pack(fill=tk.BOTH, expand=True, pady=10)

# Load saved emails on startup
load_emails()

root.mainloop()
