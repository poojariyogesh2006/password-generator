import tkinter as tk
from tkinter import messagebox
import random
import string

# ---------------- Security Check ----------------
def check_security(password):

    if len(password) < 8:
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    if not any(c in string.punctuation for c in password):
        return False

    # No consecutive repeated characters
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return False

    return True


# ---------------- Generate Password ----------------
def generate_password():

    try:
        length = int(length_entry.get())

        if length < 8:
            messagebox.showerror(
                "Error",
                "Password length must be at least 8"
            )
            return

        # Security rule: all character types required
        if not (upper_var.get() and lower_var.get()
                and digit_var.get() and symbol_var.get()):

            messagebox.showerror(
                "Security Rule",
                "Select Uppercase, Lowercase, Numbers and Symbols."
            )
            return

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        symbols = string.punctuation

        # Exclude Similar Characters
        if exclude_var.get():

            remove_chars = "O0Il1"

            upper = ''.join(
                c for c in upper
                if c not in remove_chars
            )

            lower = ''.join(
                c for c in lower
                if c not in remove_chars
            )

            digits = ''.join(
                c for c in digits
                if c not in remove_chars
            )

        all_chars = upper + lower + digits + symbols

        while True:

            password = [
                random.choice(upper),
                random.choice(lower),
                random.choice(digits),
                random.choice(symbols)
            ]

            while len(password) < length:
                password.append(
                    random.choice(all_chars)
                )

            random.shuffle(password)

            final_password = "".join(password)

            if check_security(final_password):
                break

        password_var.set(final_password)

        # Strength Meter
        if length < 10:
            strength_label.config(
                text="Strength: Medium"
            )

        elif length < 14:
            strength_label.config(
                text="Strength: Strong"
            )

        else:
            strength_label.config(
                text="Strength: Very Strong"
            )

        security_label.config(
            text="Security: Passed ✓"
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter a valid number"
        )


# ---------------- Copy Password ----------------
def copy_password():

    password = password_var.get()

    if password == "":
        messagebox.showwarning(
            "Warning",
            "Generate a password first"
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


# ---------------- GUI ----------------
root = tk.Tk()

root.title("Advanced Password Generator")
root.geometry("550x650")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="secure Password Generator",
    font=("Arial", 16, "bold")
).pack(pady=10)

# Length
tk.Label(
    root,
    text="Enter Password Length"
).pack()

length_entry = tk.Entry(root)
length_entry.pack(pady=5)

# Options
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

tk.Checkbutton(
    root,
    text="Uppercase Letters (A-Z)",
    variable=upper_var
).pack(anchor="w")

tk.Checkbutton(
    root,
    text="Lowercase Letters (a-z)",
    variable=lower_var
).pack(anchor="w")

tk.Checkbutton(
    root,
    text="Numbers (0-9)",
    variable=digit_var
).pack(anchor="w")

tk.Checkbutton(
    root,
    text="Symbols (!,@,#,$,...)",
    variable=symbol_var
).pack(anchor="w")

tk.Checkbutton(
    root,
    text="Exclude Similar Characters (O,0,I,l,1)",
    variable=exclude_var
).pack(anchor="w")

# Generate Button
tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    width=25
).pack(pady=10)

# Password Display
password_var = tk.StringVar()

tk.Entry(
    root,
    textvariable=password_var,
    width=40,
    font=("Arial", 12)
).pack(pady=10)

# Copy Button
tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    width=25
).pack(pady=5)

# Strength
strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 11, "bold")
)
strength_label.pack(pady=5)

# Security Status
security_label = tk.Label(
    root,
    text="Security Status",
    font=("Arial", 11, "bold")
)
security_label.pack(pady=5)

# Security Rules
tk.Label(
    root,
    text="Security Rules",
    font=("Arial", 12, "bold")
).pack(pady=10)

rules = """
✓ Minimum password length: 8 characters

✓ At least 1 Uppercase Letter (A-Z)

✓ At least 1 Lowercase Letter (a-z)

✓ At least 1 Number (0-9)

✓ At least 1 Special Character (!,@,#,$...)

✓ No consecutive repeated characters

✓ Option to exclude confusing characters
  (O, 0, I, l, 1)

✓ Password strength validation

✓ One-click clipboard copy
"""

tk.Label(
    root,
    text=rules,
    justify="left",
    fg="green"
).pack()

root.mainloop()
