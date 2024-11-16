import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import json
from notif import NotificationSystem
from hhtp_req import check_breach

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

# Global variable to store widgets for dynamic switching
email_listbox = None
email_entry = None
results_text = None
check_button = None
new_button = None
original_button = None

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

# Function to switch to the profile view
def show_profile_view(event=None):
    
    # Clear the main frame content
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Add profile information widgets
    profile_label = ttk.Label(input_frame, text="Profile Information", font=('Helvetica', 16, 'bold'))
    profile_label.pack(pady=10)

    name_label = ttk.Label(input_frame, text="Name: John Doe")
    name_label.pack(pady=5)

    email_label = ttk.Label(input_frame, text="Email: johndoe@example.com")
    email_label.pack(pady=5)

    # Button to return to the email management view
    back_button = ttk.Button(input_frame, text="Back", command=show_email_management_view)
    back_button.pack(pady=10, fill=tk.X)

# Function to switch back to the email management view
def show_email_management_view():
    global email_listbox, email_entry, results_text, check_button, new_button, original_button  # Declare globals for shared access

    # Clear the main frame content
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Ensure the check button is hidden when switching views
    if check_button:
        check_button.pack_forget()
        

    # Re-add email management widgets
    email_label = ttk.Label(input_frame, text="Enter Email:")
    email_label.pack(pady=10)

    email_entry = ttk.Entry(input_frame, width=30)
    email_entry.pack(fill=tk.X, expand=True, pady=5)
    email_entry.bind("<Return>", add_email)  # Re-bind Enter key to add_email function

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

# Initialize the main application window
root = tk.Tk()
root.title("Email Breach Checker")
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

# Bind the circle to show profile view
canvas.tag_bind(circle, "<Button-1>", show_profile_view)

# Sidebar buttons
sidebar_settings_button = ttk.Button(sidebar, text="Settings")
sidebar_settings_button.pack(fill=tk.X, pady=5)

sidebar_passwords_button = ttk.Button(sidebar, text="Passwords")
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
