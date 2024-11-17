import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import json
from notif import NotificationSystem
from hhtp_req import check_breach
from main import check_pass
import random
import string


current_directory = f"{Path.cwd()}"
tokens = current_directory.split("/")

if tokens[-1] == "input":
    EMAILS_FILE = f"{Path.cwd()}/emails.json"
elif tokens[-1] == "HHAHHAHAHAHAHHAHA":
    EMAILS_FILE = f"{Path.cwd()}/input/emails.json"
else:
    EMAILS_FILE = f"{Path.cwd()}/emails.json"  # Default path

notifier = NotificationSystem()


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
isLoggedIn = False

def show_login_screen():
    for widget in input_frame.winfo_children():
        widget.destroy()

    login_label = ttk.Label(input_frame, text="Log In to Your Account", font=('Helvetica', 16, 'bold'))
    login_label.pack(pady=20)

    username_label = ttk.Label(input_frame, text="Username:")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(input_frame, width=30)
    username_entry.pack(pady=5)

    password_label = ttk.Label(input_frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(input_frame, width=30, show="*")
    password_entry.pack(pady=5)

    toggle_var = tk.BooleanVar(value=True)  

    def handle_toggle():
        state = "Private" if toggle_var.get() else "Public"

    toggle_button = ttk.Checkbutton(
        input_frame,
        text="Remember Me",  
        variable=toggle_var,  
        command=handle_toggle  
    )
    toggle_button.pack(pady=10)

    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username == "test" and password == "test":  
            messagebox.showinfo("Login Successful", "Welcome back!")
            isLoggedIn = True
            show_email_management_view()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    login_button = ttk.Button(input_frame, text="Log In", command=handle_login)
    login_button.pack(pady=10, fill=tk.X)

    exit_button = ttk.Button(input_frame, text="Exit", command=root.destroy)
    exit_button.pack(pady=10, fill=tk.X)

def show_settings_template():
    for widget in input_frame.winfo_children():
        widget.destroy()
    
    settings_label = ttk.Label(input_frame, text="Settings", font=('Helvetica', 16, 'bold'))
    settings_label.pack(pady=10)

    toggle_var = tk.BooleanVar(value=False)  

    def handle_toggle():
        state = "Private" if toggle_var.get() else "Public"
        print(f"Toggle state changed to {state}")  
        messagebox.showinfo("Toggle State", f"Account is now {state}")

    toggle_button = ttk.Checkbutton(
        input_frame,
        text="Enable Feature",  
        variable=toggle_var,  
        command=handle_toggle  
    )
    toggle_button.pack(pady=10)

    additional_label = ttk.Label(input_frame, text="More settings coming soon...", font=('Helvetica', 12))
    additional_label.pack(pady=10)
      


def generate_random_password():
    length = 16
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def show_random_password():
    random_password = generate_random_password()
    password_result_text.delete(1.0, tk.END)
    password_result_text.insert(tk.END, f"Your new random password is:\n{random_password}")
    remove_password_prompt()

def remove_password_prompt():
    if password_prompt_label:
        password_prompt_label.destroy()
    if yes_button:
        yes_button.destroy()
    if no_button:
        no_button.destroy()

def show_password_prompt():
    global password_prompt_label, yes_button, no_button
    
    remove_password_prompt()
    
    password_prompt_label = ttk.Label(input_frame, text="Do you want a random new password?", 
                                    font=('Helvetica', 12))
    password_prompt_label.pack(pady=10)
    
    button_frame = ttk.Frame(input_frame)
    button_frame.pack(pady=5)
    
    yes_button = ttk.Button(button_frame, text="Yes", command=show_random_password)
    yes_button.pack(side=tk.LEFT, padx=5)
    
    no_button = ttk.Button(button_frame, text="No", command=remove_password_prompt)
    no_button.pack(side=tk.LEFT, padx=5)

def load_emails():
    try:
        with open(EMAILS_FILE, "r") as file:
            emails = json.load(file).get("emails", [])
            for email in emails:
                email_listbox.insert(tk.END, email)
    except FileNotFoundError:
        pass

def save_emails():
    emails = email_listbox.get(0, tk.END)
    Path(EMAILS_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(EMAILS_FILE, "w") as file:
        json.dump({"emails": list(emails)}, file)

def add_email(event=None):
    email = email_entry.get().strip()
    if email and email not in email_listbox.get(0, tk.END):
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
        save_emails()
    else:
        messagebox.showwarning("Invalid Email", "Please enter a valid and unique email.")

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
    global processing_done
    processing_done = False  
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
                check_button.config(text="Check Breaches", command=check_all_emails, state='normal')
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

    check_button.config(text="Checking", command=None, state='disabled')
    show_loading_animation()
    process_emails()

def show_email_management_view():
    global email_listbox, email_entry, results_text, check_button, sidebar_passwords_button

    for widget in input_frame.winfo_children():
        widget.destroy()

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

    load_emails()

    sidebar_passwords_button.config(text="Passwords", command=show_password_view)

def check_password():
    password = password_entry.get().strip()
    if password:
        result = check_pass(password)
        password_result_text.delete(1.0, tk.END)
        password_result_text.insert(tk.END, result + "\n")
        password_entry.delete(0, tk.END)
        show_password_prompt()
    else:
        messagebox.showwarning("Invalid Password", "Please enter a valid password.")

def show_logout_screen():
    for widget in input_frame.winfo_children():
        widget.destroy()

    logout_label = ttk.Label(input_frame, text="You must log in to use the app.", font=('Helvetica', 16, 'bold'))
    logout_label.pack(pady=20)

    login_button = ttk.Button(input_frame, text="Log In", command=show_login_screen)
    login_button.pack(pady=10, fill=tk.X)

    exit_button = ttk.Button(input_frame, text="Exit", command=root.destroy)
    exit_button.pack(pady=10, fill=tk.X)


def show_password_view(event=None):
    global password_entry, password_result_text, sidebar_passwords_button

    for widget in input_frame.winfo_children():
        widget.destroy()

    password_label = ttk.Label(input_frame, text="Enter Password to Check:", font=('Helvetica', 16, 'bold'))
    password_label.pack(pady=10)

    password_entry = ttk.Entry(input_frame, width=30, font=('Helvetica', 12))
    password_entry.pack(fill=tk.X, pady=5)
    password_entry.bind("<Return>", lambda event: show_password_in_textbox())

    check_button = ttk.Button(input_frame, text="Check Password", command=check_password)
    check_button.pack(pady=10, fill=tk.X)

    password_result_text = tk.Text(input_frame, font=('Helvetica', 12), height=5, wrap=tk.WORD)
    password_result_text.pack(fill=tk.BOTH, expand=True, pady=10)

    sidebar_passwords_button.config(text="Emails", command=show_email_management_view)

def show_password_in_textbox():
    password = password_entry.get().strip()
    if password:
        password_result_text.delete(1.0, tk.END)
        password_result_text.insert(tk.END, f"Password entered: {password}\n")
        store_password(password)
    else:
        messagebox.showwarning("Invalid Password", "Please enter a valid password.")    

def store_password(password):
    passwd_file = 'passwd.json'
    try:
        with open(passwd_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(password)

    with open(passwd_file, 'w') as file:
        json.dump(data, file)

root = tk.Tk()
root.title("Breach Checker")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#2c3e50")

style = ttk.Style()
style.theme_use('alt')

style.configure('TFrame', background='#34495e')
style.configure('TLabel', background='#34495e', foreground='white', font=('Helvetica', 12))
style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 12, 'bold'), padding=10)
style.configure('TEntry', font=('Helvetica', 12), padding=10)
style.configure('TListbox', font=('Helvetica', 12), background='#ecf0f1')

sidebar = ttk.Frame(root, width=200, relief='sunken', padding=(20, 20))
sidebar.pack(side=tk.LEFT, fill=tk.Y)

canvas = tk.Canvas(sidebar, width=150, height=150, bg='#34495e', bd=0, highlightthickness=0)
canvas.pack(pady=(0, 20))
circle = canvas.create_oval(20, 20, 130, 130, fill="lightblue", outline="white", width=2)

sidebar_settings_button = ttk.Button(sidebar, text="Settings",command=show_settings_template)
sidebar_settings_button.pack(fill=tk.X, pady=5)

sidebar_passwords_button = ttk.Button(sidebar, text="Passwords", command=show_password_view)
sidebar_passwords_button.pack(fill=tk.X, pady=5)

if isLoggedIn == True :
    sidebar_logout_button = ttk.Button(sidebar, text="Logout", command=show_logout_screen)
    isLoggedIn == False
    sidebar_logout_button.pack(fill=tk.X, pady=5)
elif isLoggedIn == False :
    sidebar_logout_button = ttk.Button(sidebar, text="Log In", command=show_login_screen)
    isLoggedIn == True
    sidebar_logout_button.pack(fill=tk.X, pady=5)

sidebar_exit_button = ttk.Button(sidebar, text="EXIT",command=root.destroy)
sidebar_exit_button.pack(fill=tk.X,pady=5)
input_frame = ttk.Frame(root, padding="20 20 20 20")
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.RIGHT)

show_email_management_view()

root.mainloop()