import tkinter as tk
from tkinter import messagebox


# Dummy function to simulate breach checking
def check_breach(email):
    # Simulate breach checking logic (replace with actual API calls later)
    breached_emails = ["test@example.com", "user@breach.com"]
    if email in breached_emails:
        return f"{email}: Breached!"
    return f"{email}: No breach found."


# Add email to the list
def add_email():
    email = email_entry.get().strip()
    if email and email not in email_listbox.get(0, tk.END):
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid Email", "Enter a valid email or avoid duplicates.")


# Check breaches for all emails
def check_all_emails():
    emails = email_listbox.get(0, tk.END)
    if not emails:
        messagebox.showinfo("No Emails", "Add some emails first.")
        return

    results_text.delete(1.0, tk.END)  # Clear previous results
    for email in emails:
        result = check_breach(email)
        results_text.insert(tk.END, result + "\n")


# GUI Setup
root = tk.Tk()
root.title("Email Breach Checker")
root.geometry("500x400")

# Input Area
email_label = tk.Label(root, text="Email:")
email_label.pack(pady=5)

email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Email", command=add_email)
add_button.pack(pady=5)

# Email List
email_listbox = tk.Listbox(root, height=10, width=40)
email_listbox.pack(pady=10)

# Check Breaches Button
check_button = tk.Button(root, text="Check Breaches", command=check_all_emails)
check_button.pack(pady=10)

# Results Display
results_text = tk.Text(root, height=10, width=60)
results_text.pack(pady=10)

# Run the Application
root.mainloop()
