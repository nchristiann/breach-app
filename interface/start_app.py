import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from pathlib import Path
import json
from notif import NotificationSystem
from hhtp_req import check_breach

current_directory = f"{Path.cwd()}"
tokens = current_directory.split("/")

if tokens[-1] == "input":
    EMAILS_FILE = f"{Path.cwd()}/emails.json"
elif tokens[-1] == "HHAHHAHAHAHAHHAHA":
    EMAILS_FILE = f"{Path.cwd()}/input/emails.json"
else:
    EMAILS_FILE = f"{Path.cwd()}/emails.json"  # Default path

notifier = NotificationSystem()

def load_emails():
    try:
        with open(EMAILS_FILE, "r") as file:
            emails = json.load(file)["emails"]
            for email in emails:
                email_listbox.insert(tk.END, email)
    except FileNotFoundError:
        pass

def save_emails():
    emails = email_listbox.get(0, tk.END)
    with open(EMAILS_FILE, "w") as file:
        json.dump({"emails": list(emails)}, file)

def add_email():
    email = email_entry.get().strip()
    if email and email not in email_listbox.get(0, tk.END):
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
        save_emails()

def delete_email():
    selected_email = email_listbox.curselection()
    if selected_email:
        email_listbox.delete(selected_email)
        save_emails()

def check_all_emails():
    emails = email_listbox.get(0, tk.END)
    if not emails:
        return

    results_text.delete(1.0, tk.END)
    for email in emails:
        result = check_breach(email)
        if "Breached!" in result:
            notifier.send_notification("Breach Alert", f"{email} has been breached!")
        results_text.insert(tk.END, result + "\n")

root = tk.Tk()
root.title("Email Breach Checker")
root.geometry("800x800")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
style.configure('TButton', background='#007acc', foreground='white', font=('Arial', 10, 'bold'))
style.configure('TEntry', font=('Arial', 12))

input_frame = ttk.Frame(root, padding="10 10 10 10")
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

email_label = ttk.Label(input_frame, text="Email:")
email_label.pack(pady=5)

email_entry = ttk.Entry(input_frame)
email_entry.pack(fill=tk.BOTH, expand=True, pady=5)

add_button = ttk.Button(input_frame, text="Add Email", command=add_email)
add_button.pack(pady=5)

delete_button = ttk.Button(input_frame, text="Delete Email", command=delete_email)
delete_button.pack(pady=5)

email_listbox = tk.Listbox(input_frame, font=('Arial', 12))
email_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

check_button = ttk.Button(input_frame, text="Check Breaches", command=check_all_emails)
check_button.pack(pady=5)

results_text = tk.Text(input_frame, font=('Arial', 12))
results_text.pack(fill=tk.BOTH, expand=True, pady=5)

load_emails()
root.mainloop()