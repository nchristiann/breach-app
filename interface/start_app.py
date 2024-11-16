import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import json
from notif import NotificationSystem
from hhtp_req import check_breach
import random
import string

# Determine the current directory and emails file path
current_directory = f"{Path.cwd()}"
tokens = current_directory.split("/")

if tokens[-1] == "input":
    EMAILS_FILE = f"{Path.cwd()}/emails.json"
elif tokens[-1] == "HHAHHAHAHAHAHHAHA":
    EMAILS_FILE = f"{Path.cwd()}/input/emails.json"
else:
    EMAILS_FILE = f"{Path.cwd()}/emails.json"  # Default path

notifier = NotificationSystem()

# Global variables to store widgets for dynamic switching
email_listbox = None
email_entry = None
results_text = None
password_entry = None
password_result_text = None
check_button = None
sidebar_passwords_button = None
password_prompt_label = None
yes_button = None
no_button = None

def generate_random_password():
    # Generate a strong random password
    length = 16
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def show_random_password():
    # Generate and show the random password
    random_password = generate_random_password()
    password_result_text.delete(1.0, tk.END)
    password_result_text.insert(tk.END, f"Your new random password is:\n{random_password}")
    remove_password_prompt()

def remove_password_prompt():
    # Remove the prompt and buttons
    if password_prompt_label:
        password_prompt_label.destroy()
    if yes_button:
        yes_button.destroy()
    if no_button:
        no_button.destroy()

def show_password_prompt():
    global password_prompt_label, yes_button, no_button
    
    # Remove any existing prompt and buttons first
    remove_password_prompt()
    
    # Create new prompt and buttons
    password_prompt_label = ttk.Label(input_frame, text="Do you want a random new password?", 
                                    font=('Helvetica', 12))
    password_prompt_label.pack(pady=10)
    
    button_frame = ttk.Frame(input_frame)
    button_frame.pack(pady=5)
    
    yes_button = ttk.Button(button_frame, text="Yes", command=show_random_password)
    yes_button.pack(side=tk.LEFT, padx=5)
    
    no_button = ttk.Button(button_frame, text="No", command=remove_password_prompt)
    no_button.pack(side=tk.LEFT, padx=5)

# Function to load emails from the file
def load_emails():
    try:
        with open(EMAILS_FILE, "r") as file:
            emails = json.load(file).get("emails", [])
            for email in emails:
                email_listbox.insert(tk.END, email)
    except FileNotFoundError:
        pass

# Function to save emails to the file
def save_emails():
    emails = email_listbox.get(0, tk.END)
    Path(EMAILS_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(EMAILS_FILE, "w") as file:
        json.dump({"emails": list(emails)}, file)

# Function to add an email
def add_email(event=None):
    email = email_entry.get().strip()
    if email and email not in email_listbox.get(0, tk.END):
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
        save_emails()
    else:
        messagebox.showwarning("Invalid Email", "Please enter a valid and unique email.")

# Function to delete a selected email
def delete_email():
    selected_email = email_listbox.curselection()
    if selected_email:
        email_listbox.delete(selected_email)
        save_emails()

# Function to check breaches for all emails
def check_all_emails():
    emails = email_listbox.get(0, tk.END)
    if not emails:
        return

    results_text.delete(1.0, tk.END)
    global processing_done
    processing_done = False  # Flag to control the animation

    def check_email(email):
        try:
            result = check_breach(email)
            if "Breached!" in result:
                notifier.send_notification("Breach Alert", f"{email} has been breached!")
            return result
        except Exception as e:
            return f"Error checking {email}: {str(e)}"

    def process_emails(index=0):
        if index < len(emails):
            email = emails[index]
            result = check_email(email)
            results_text.insert(tk.END, result + "\n")
            root.after(1, show_loading_animation)
            if index + 1 < len(emails):
                root.after(6000, process_emails, index + 1)
            else:
                results_text.insert(tk.END, "All emails checked.\n")
                check_button.config(text="Check Breaches", command=check_all_emails)
                global processing_done
                processing_done = True 
        else:
            pass

    def show_loading_animation():
        loading_text = "Checking"
        def animate(i=0):
            if processing_done:
                return
            check_button.config(text=loading_text + "." * (i % 4))
            root.after(600, animate, i + 1)
        animate()

    check_button.config(text="Checking", command=None)
    show_loading_animation()
    process_emails()

# Function to switch back to the email management view
def show_email_management_view():
    global email_listbox, email_entry, results_text, check_button, sidebar_passwords_button

    # Clear the main frame content
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Re-add email management widgets
    email_label = ttk.Label(input_frame, text="Enter Email:")
    email_label.pack(pady=10)

    email_entry = ttk.Entry(input_frame, width=30)
    email_entry.pack(fill=tk.X, expand=True, pady=5)
    email_entry.bind("<Return>", add_email)

    delete_button = ttk.Button(input_frame, text="Delete Email", command=delete_email)
    delete_button.pack(pady=10, fill=tk.X)

    email_listbox = tk.Listbox(input_frame, font=('Helvetica', 12), height=8)
    email_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

    check_button = ttk.Button(input_frame, text="Check Breaches", command=check_all_emails)
    check_button.pack(pady=10, fill=tk.X)

    results_text = tk.Text(input_frame, font=('Helvetica', 12), height=10, wrap=tk.WORD)
    results_text.pack(fill=tk.BOTH, expand=True, pady=10)

    # Reload emails into the listbox
    load_emails()

    # Change the sidebar button text to "Passwords" and update the command
    sidebar_passwords_button.config(text="Passwords", command=show_password_view)

# Function to check password breach
def check_password():
    password = password_entry.get().strip()
    if password:
        result = check_breach(password)
        password_result_text.delete(1.0, tk.END)
        password_result_text.insert(tk.END, result + "\n")
        password_entry.delete(0, tk.END)
        # Show the random password prompt after checking
        show_password_prompt()
    else:
        messagebox.showwarning("Invalid Password", "Please enter a valid password.")

# Function to switch to the password checking view
def show_password_view(event=None):
    global password_entry, password_result_text, sidebar_passwords_button

    # Clear the main frame content
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Add password checking widgets
    password_label = ttk.Label(input_frame, text="Enter Password to Check:", font=('Helvetica', 16, 'bold'))
    password_label.pack(pady=10)

    password_entry = ttk.Entry(input_frame, width=30, font=('Helvetica', 12))
    password_entry.pack(fill=tk.X, pady=5)
    password_entry.bind("<Return>", lambda event: check_password())

    check_button = ttk.Button(input_frame, text="Check Password", command=check_password)
    check_button.pack(pady=10, fill=tk.X)

    password_result_text = tk.Text(input_frame, font=('Helvetica', 12), height=5, wrap=tk.WORD)
    password_result_text.pack(fill=tk.BOTH, expand=True, pady=10)

    # Change the sidebar button text to "Emails" and update the command
    sidebar_passwords_button.config(text="Emails", command=show_email_management_view)

# Initialize the main application window
root = tk.Tk()
root.title("Breach Checker")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Configure styles for the application
style = ttk.Style()
style.theme_use('alt')

style.configure('TFrame', background='#34495e')
style.configure('TLabel', background='#34495e', foreground='white', font=('Helvetica', 12))
style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 12, 'bold'), padding=10)
style.configure('TEntry', font=('Helvetica', 12), padding=10)
style.configure('TListbox', font=('Helvetica', 12), background='#ecf0f1')

# Create a frame for the sidebar
sidebar = ttk.Frame(root, width=200, relief='sunken', padding=(20, 20))
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Add a canvas for the profile picture circle at the top of the sidebar
canvas = tk.Canvas(sidebar, width=150, height=150, bg='#34495e', bd=0, highlightthickness=0)
canvas.pack(pady=(0, 20))
circle = canvas.create_oval(20, 20, 130, 130, fill="lightblue", outline="white", width=2)

# Sidebar buttons
sidebar_settings_button = ttk.Button(sidebar, text="Settings")
sidebar_settings_button.pack(fill=tk.X, pady=5)

sidebar_passwords_button = ttk.Button(sidebar, text="Passwords", command=show_password_view)
sidebar_passwords_button.pack(fill=tk.X, pady=5)

sidebar_logout_button = ttk.Button(sidebar, text="Logout")
sidebar_logout_button.pack(fill=tk.X, pady=5)

# Main frame for email management
input_frame = ttk.Frame(root, padding="20 20 20 20")
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.RIGHT)

# Show the email management view by default
show_email_management_view()

# Run the application
root.mainloop()