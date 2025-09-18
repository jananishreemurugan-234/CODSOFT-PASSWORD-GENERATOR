import tkinter as tk
from tkinter import messagebox, filedialog
import secrets
import string

def build_charset(use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous):
    ambiguous = set('Il1O0')
    charset = []
    if use_lower:
        charset.extend(list(string.ascii_lowercase))
    if use_upper:
        charset.extend(list(string.ascii_uppercase))
    if use_digits:
        charset.extend(list(string.digits))
    if use_symbols:
        charset.extend(list('!@#$%^&*()-_=+[]{};:,.<>?/'))
    if not charset:
        raise ValueError("At least one character set must be selected.")
    if avoid_ambiguous:
        charset = [c for c in charset if c not in ambiguous]
    return ''.join(charset)


def generate_password(length, charset):
    return ''.join(secrets.choice(charset) 
    for _ in range(length))


def generate():
    try:
        length = int(length_var.get())
        count = int(count_var.get())
        charset = build_charset(
            lower_var.get(),
            upper_var.get(),
            digits_var.get(),
            symbols_var.get(),
            ambiguous_var.get()
        )
        passwords = [generate_password(length, charset) 
                     for _ in range(count)]
        output_box.delete(1.0, tk.END)
        for i, p in enumerate(passwords, start=1):
            output_box.insert(tk.END, f"{i}. {p}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_to_file():
    content = output_box.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No passwords to save.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Passwords saved to {filename}")
        except OSError as e:
            messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Codsoft Task 3: Password Generator")
root.geometry("550x550")
root.configure(bg="#b008fe")

# Frame for inputs
frame = tk.Frame(root, bg="#efe2fb")
frame.pack(pady=10)

label_style = {"bg": "#efe2fb", "fg": "#000000", "font": ("Arial", 11, "bold")}
entry_style = {"bg": "#ffffff", "fg": "#000000", "font": ("Arial", 11)}

# Length input
tk.Label(frame, text="Password Length:", **label_style).grid(row=0, column=0, sticky="w")
length_var = tk.StringVar(value="12")
tk.Entry(frame, textvariable=length_var, width=5, **entry_style).grid(row=0, column=1)

# Count input
tk.Label(frame, text="Number of Passwords:", **label_style).grid(row=1, column=0, sticky="w")
count_var = tk.StringVar(value="1")
tk.Entry(frame, textvariable=count_var, width=5, **entry_style).grid(row=1, column=1)

# Checkboxes
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
ambiguous_var = tk.BooleanVar(value=True)

check_style = {"bg": "#efe2fb", "fg": "#8210FC", "font": ("Arial", 10)}

tk.Checkbutton(frame, text="Include lowercase (a-z)", variable=lower_var, **check_style).grid(row=2, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Include uppercase (A-Z)", variable=upper_var, **check_style).grid(row=3, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Include digits (0-9)", variable=digits_var, **check_style).grid(row=4, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Include symbols (@#$%)", variable=symbols_var, **check_style).grid(row=5, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Avoid ambiguous (I, l, 1, O, 0)", variable=ambiguous_var, **check_style).grid(row=6, column=0, columnspan=2, sticky="w")

# Buttons
button_style = {"bg": "#fb58af", "fg": "white", "font": ("Arial", 11, "bold"), "relief": "raised", "bd": 3, "width": 20}

tk.Button(root, text="Generate Passwords", command=generate, **button_style).pack(pady=10)
tk.Button(root, text="Save to File", command=save_to_file, **button_style).pack(pady=5)

# Output Box
output_box = tk.Text(root, height=12, width=60, bg="#ffffff", fg="#000000", font=("Courier New", 11))
output_box.pack(pady=10)

root.mainloop()